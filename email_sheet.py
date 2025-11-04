import gspread

SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/14V5NBooFYgg144Zsxzgq7E8R9SIA-JhOZynAlssEKoY/edit?usp=sharing"

subjects = ["sip","bp","lp","sp","aor1","oop","oopj","pj","dmat","aip","uur"]

sh = gspread.public().open_by_url(SPREADSHEET_URL)

for subj in subjects:
    try:
        
        ws = sh.worksheet(subj)

        
        emails = [e.strip() for e in ws.col_values(1) if e.strip()]

        
        filename = f"{subj}_emails.md"
        with open(filename, "w") as f:
            f.write("\n".join(emails))

        print(f"✅ {len(emails)} emails saved to {filename}")

    except gspread.exceptions.WorksheetNotFound:
        print(f"⚠️ Sheet '{subj}' not found, skipping...")
