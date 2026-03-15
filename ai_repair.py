import os
import requests
from litellm_client import LiteLLMClient

# Keep global config or move into the class
SONAR_TOKEN = os.getenv("SONAR_TOKEN")
SONAR_PROJECT = "simrank01_coderabbbit-test-main"
CUSTOM_API_BASE = os.getenv("AI_API_BASE")
MODEL_NAME = "AEM" 

class SonarRepairAgent:
    def __init__(self, litellm: LiteLLMClient):
        # self now correctly refers to the instance of this class
        self.litellm = litellm

    def run_agent(self):
        print(f"--- Starting Agent ---")
        print(f"Project Key: {SONAR_PROJECT}")
        
        # 1. Fetch Issues
        url = f"https://sonarcloud.io/api/issues/search?componentKeys={SONAR_PROJECT}&resolved=false"
        response = requests.get(url, auth=(SONAR_TOKEN, ''))
        
        if response.status_code != 200:
            print(f"❌ Error talking to SonarCloud: {response.status_code}")
            return

        issues = response.json().get('issues', [])
        print(f"Found {len(issues)} open issues in SonarCloud.")

        if not issues:
            print("✅ No issues found by the script.")
            return

        for issue in issues[:5]:
            file_path = issue['component'].split(':')[-1]
            error_msg = issue['message']
            
            # Skip the script itself to prevent accidental corruption
            if file_path == "ai_repair.py":
                continue

            if os.path.exists(file_path):
                print(f"🛠️ Fixing {file_path}...")
                with open(file_path, 'r') as f:
                    old_code = f.read()

                system_message = (
                    "You are a Senior Technical Architect specializing in Adobe Experience Manager (AEM) "
                    "and Python automation. Your goal is to fix SonarQube security vulnerabilities and bugs. "
                    "Rules:\n"
                    "1. Focus on security: fix SQL injections, hardcoded secrets, and unsafe eval() calls.\n"
                    "2. Return ONLY the corrected code. No explanations, no markdown backticks."
                )
                
                user_message = f"Fix the SonarQube issue: '{error_msg}' in the file '{file_path}'.\n\nCODE:\n{old_code}"
                
                # Using the litellm client instance stored in self
                ai_response = self.litellm.chat(
                    model=MODEL_NAME,
                    system_prompt=system_message,
                    user_prompt=user_message
                )
                
                # Check if response has content before stripping
                if ai_response and ai_response.choices:
                    new_code = ai_response.choices[0].message.content.strip()

                    with open(file_path, 'w') as f:
                        f.write(new_code)
                    print(f"✅ Successfully updated {file_path}")
            else:
                print(f"⚠️ Could not find file locally: {file_path}")

if __name__ == "__main__":
    # 1. Initialize the external client
    client = LiteLLMClient() 
    
    # 2. Create an instance of your agent and pass the client
    agent = SonarRepairAgent(litellm=client)
    
    # 3. Call the method on the instance
    agent.run_agent()
