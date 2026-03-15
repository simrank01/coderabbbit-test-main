import os
import requests
from litellm import completion

# 1. Configuration
SONAR_TOKEN = os.getenv("SONAR_TOKEN")
SONAR_PROJECT = "YOUR_PROJECT_KEY_HERE"

# 2. Pick your model (LiteLLM supports 'claude-3-5-sonnet', 'gpt-4o', 'gemini/gemini-1.5-pro', etc.)
# You just change this string to switch AI brains!
MODEL_NAME = "AEM" 

def get_issues():
    url = f"https://sonarcloud.io/api/issues/search?componentKeys={SONAR_PROJECT}&resolved=false"
    response = requests.get(url, auth=(SONAR_TOKEN, ''))
    return response.json().get('issues', [])

def fix_code(error_message, code_content):
    prompt = f"""
    Fix the following SonarQube issue: "{error_message}"
    Return ONLY the corrected code. No explanations, no markdown.

    CODE:
    {code_content}
    """

    # LiteLLM uses a simple format that works for ANY provider
    response = completion(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    
    return response.choices[0].message.content.strip()

def run_agent():
    issues = get_issues()
    for issue in issues[:5]:
        file_path = issue['component'].split(':')[-1]
        error_msg = issue['message']
        
        if os.path.exists(file_path):
            print(f" LiteLLM ({MODEL_NAME}) is fixing: {file_path}")
            with open(file_path, 'r') as f:
                old_code = f.read()

            new_code = fix_code(error_msg, old_code)

            with open(file_path, 'w') as f:
                f.write(new_code)

if __name__ == "__main__":
    run_agent()
