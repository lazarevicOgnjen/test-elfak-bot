import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import json

def setup_sheets():
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    
    creds_json = os.environ.get('GOOGLE_CREDENTIALS_JSON')
    creds_dict = json.loads(creds_json)
    
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    return gspread.authorize(creds)

def main():
    client = setup_sheets()
    
    YOUR_SHEET_NAME = "ELFAK sheet" 
    
    courses = ['bp', 'sp', 'pj', 'oopj', 'lp', 'oop', 'aor1', 'dmat']
    
    try:
        sheet = client.open(YOUR_SHEET_NAME)
        
        for course in courses:
            worksheet = sheet.worksheet(course)
            emails = worksheet.col_values(1)
            
            # Clean emails
            emails = [email.strip() for email in emails if email.strip() and '@' in email]
            
            # Save to .md file
            filename = f"{course}_emails.md"
            with open(filename, 'w') as f:
                for email in sorted(set(emails)):
                    f.write(f"{email}\n")
            
            print(f"✅ {course}: {len(emails)} emails")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
