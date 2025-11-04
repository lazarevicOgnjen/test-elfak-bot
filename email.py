import os
import json
import gspread

credentials_json = os.environ.get("GOOGLE_CREDENTIALS_JSON")
if not credentials_json:
    raise RuntimeError("GOOGLE_CREDENTIALS_JSON not set")

credentials_dict = json.loads(credentials_json)

gc = gspread.service_account_from_dict(credentials_dict)

SPREADSHEET_NAME = "Elfak bot"
sh = gc.open(SPREADSHEET_NAME)

subjects = ["sip","bp","lp","sp","aor1","oop","oopj","pj","dmat","aip","uur"]

for subj in subjects:
    try:
        ws = sh.worksheet(subj)
    except gspread.exceptions.WorksheetNotFound:
        print(f"⚠️ Sheet '{subj}' not found, skipping...")
        continue

    emails = [e.strip() for e in ws.col_values(1) if e.strip()]

    filename = f"{subj}_emails.md"
    with open(filename, "w") as f:
        f.write("\n".join(emails))

    print(f"✅ {len(emails)} emails saved to {filename}")
