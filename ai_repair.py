import os
import requests
from litellm import completion

# CONFIGURATION
SONAR_TOKEN = os.getenv("SONAR_TOKEN")
SONAR_PROJECT = "simrank01_coderabbbit-test-main" # <-- DOUBLE CHECK THIS
MODEL_NAME = "AEM" 

def run_agent():
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
            prompt = f"Fix this SonarQube issue: {error_msg}\n\nCode:\n{old_code}"
            ai_response = completion(
                model=MODEL_NAME,
                messages=[{"role": "user", "content": prompt}],
                temperature=0
            )
            new_code = ai_response.choices[0].message.content.strip()

            # Save fix
            with open(file_path, 'w') as f:
                f.write(new_code)
            print(f"✅ Successfully updated {file_path}")
        else:
            print(f"⚠️ Could not find file locally: {file_path}")

if __name__ == "__main__":
    run_agent()
