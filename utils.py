import os
import json
from datetime import datetime

def create_test_report(test_name, url, success, messages, error=None):
    report = {
        "test_name": test_name,
        "url": url,
        "timestamp": datetime.now().isoformat(),
        "success": success,
        "messages": messages,
        "error": str(error) if error else None
    }
    return report

def save_test_report(report, filename=None):
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"test_report_{timestamp}.json"
    
    with open(filename, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"Test report saved to: {filename}")
    return filename

def load_test_config(config_file="test_config.json"):
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            return json.load(f)
    return {}

def validate_environment():
    required_vars = ["ORGO_API_KEY"]
    optional_vars = ["ANTHROPIC_API_KEY"]
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
    
    for var in optional_vars:
        if not os.getenv(var):
            print(f"⚠️  Warning: {var} not set. Using default provider.")
    
    print("✅ Environment validation passed")
    return True

def get_common_test_prompts():
    return {
        "login_test": """
        Perform a login test:
        1. Open Firefox browser
        2. Navigate to the provided URL
        3. Look for login form fields (username/email and password)
        4. Fill username field with 'testuser'
        5. Fill password field with 'testpass'
        6. Click the login/submit button
        7. Wait for page to load
        8. Take a screenshot
        9. Check if login was successful (look for dashboard, welcome message, or error)
        10. Report the result
        """,
        
        "navigation_test": """
        Perform a navigation test:
        1. Open Firefox browser
        2. Navigate to the provided URL
        3. Take a screenshot of the initial page
        4. Check if the page loads correctly
        5. Look for navigation elements (menu, links)
        6. Click on a main navigation link if available
        7. Take another screenshot
        8. Verify the navigation worked
        9. Report the result
        """,
        
        "form_test": """
        Perform a form submission test:
        1. Open Firefox browser
        2. Navigate to the provided URL
        3. Look for any form on the page
        4. Fill out form fields with test data
        5. Submit the form
        6. Take a screenshot of the result
        7. Check if submission was successful
        8. Report the result
        """
    } 