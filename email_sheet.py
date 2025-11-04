from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os

SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/14V5NBooFYgg144Zsxzgq7E8R9SIA-JhOZynAlssEKoY/edit"

# Folder to save emails
os.makedirs("emails", exist_ok=True)

driver = webdriver.Chrome()
driver.get(SPREADSHEET_URL)
time.sleep(5)  # wait for page to load

# Get all sheet tabs
tabs = driver.find_elements(By.CSS_SELECTOR, ".docs-sheet-tab")  # tab buttons at bottom

for tab in tabs:
    tab_name = tab.text.strip()
    tab.click()
    time.sleep(2)  # wait for tab content to load

    # Get first column values
    cells = driver.find_elements(By.CSS_SELECTOR, 'div[row] > div[cell="0"]')  # simplified selector
    emails = [c.text.strip() for c in cells if c.text.strip()]

    filename = f"{tab_name}_emails.md"
    with open(filename, "w") as f:
        f.write("\n".join(emails))
    print(f"✅ {len(emails)} emails saved to {filename}")

driver.quit()
