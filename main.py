import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import json

def setup_google_sheets():
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    
    creds_json = os.environ.get('GOOGLE_CREDENTIALS_JSON')
    creds_dict = json.loads(creds_json)
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    return gspread.authorize(creds)

def get_sheet_emails(client, sheet_name):
    """Get all emails from a specific sheet"""
    try:
        sheet = client.open("YOUR_MAIN_SHEET_NAME").worksheet(sheet_name)
        emails = sheet.col_values(1)  # Get first column
        # Clean up - remove empty values, keep only emails
        emails = [email.strip() for email in emails if email.strip() and '@' in email]
        return list(set(emails))  # Remove duplicates
    except Exception as e:
        print(f"Error reading {sheet_name}: {e}")
        return []

def main():
    client = setup_google_sheets()
    
    courses = ['subscribers_bp', 'subscribers_sp', 'subscribers_pj', 
               'subscribers_oopj', 'subscribers_lp', 'subscribers_oop', 'subscribers_aor1']
    
    course_mapping = {
        'subscribers_bp': 'bp',
        'subscribers_sp': 'sp',
        'subscribers_pj': 'pj',
        'subscribers_oopj': 'oopj',
        'subscribers_lp': 'lp',
        'subscribers_oop': 'oop',
        'subscribers_aor1': 'aor1'
    }
    
    for sheet_name in courses:
        emails = get_sheet_emails(client, sheet_name)
        course_code = course_mapping[sheet_name]
        
        # Save to .md file
        filename = f"{course_code}_emails.md"
        with open(filename, 'w') as f:
            for email in sorted(emails):
                f.write(f"{email}\n")
        
        print(f"✅ {course_code}: {len(emails)} emails")
    
    print("🎯 All email files updated from Google Sheets!")

if __name__ == "__main__":
    main()
