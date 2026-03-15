import os
import requests
from litellm_client import LiteLLMClient

# CONFIGURATION
SONAR_TOKEN = os.getenv("SONAR_TOKEN")
SONAR_PROJECT = "simrank01_coderabbbit-test-main" # <-- DOUBLE CHECK THIS
CUSTOM_API_BASE = os.getenv("AI_API_BASE")
MODEL_NAME = "AEM" 

def __init__(self, litellm : LiteLLMClient):
    self.litellm = litellm;
    
def run_agent(self):
    print(f"--- Starting Agent ---")
    print(f"Project Key: {SONAR_PROJECT}")
    
    # 1. Fetch Issues
    url = f"https://sonarcloud.io/api/issues/search?componentKeys={SONAR_PROJECT}&resolved=false"
    response = requests.get(url, auth=(SONAR_TOKEN, ''))
    
    if response.status_code != 200:
        print(f"❌ Error talking to SonarCloud: {response.status_code}")
        print(response.text)
        return

    issues = response.json().get('issues', [])
    print(f"Found {len(issues)} open issues in SonarCloud.")

    if not issues:
        print("✅ No issues found by the script. Check your Project Key!")
        return

    for issue in issues[:5]:
        # Clean the file path
        component = issue['component']
        file_path = component.split(':')[-1]
        error_msg = issue['message']
        
        print(f"Checking file: {file_path}")

        if os.path.exists(file_path):
            print(f"🛠️ Fixing {file_path}...")
            with open(file_path, 'r') as f:
                old_code = f.read()

            # Ask AI for fix
            system_message = (
                    "You are a Senior Technical Architect specializing in Adobe Experience Manager (AEM) "
                    "and Python automation. Your goal is to fix SonarQube security vulnerabilities and bugs. "
                    "Rules:\n"
                    "1. Focus on security: fix SQL injections, hardcoded secrets, and unsafe eval() calls.\n"
                    "2. Maintain high performance and clean code standards.\n"
                    "3. Return ONLY the corrected code. No explanations, no markdown backticks.\n"
                    "4. Keep the original logic intact unless it is inherently broken."
            )
            
        
            user_message = f"Fix the SonarQube issue: '{error_msg}' in the file '{file_path}'.\n\nCODE:\n{old_code}"
            
            ai_response = self.litellm.chat(
                model=MODEL_NAME,
                system_prompt = system_message,
                user_prompt = user_message
                
            )
            new_code = ai_response.choices[0].message.content.strip()

            # Save fix
            with open(file_path, 'w') as f:
                f.write(new_code)
            print(f"✅ Successfully updated {file_path}")
        else:
            print(f"⚠️ Could not find file locally: {file_path}")

if __name__ == "__main__":
    run_agent(self)
