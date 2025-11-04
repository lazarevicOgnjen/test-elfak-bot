from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import os

# Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.binary_location = "/usr/bin/google-chrome"

# Chrome driver setup
browser_driver = Service('/usr/bin/chromedriver')

# Start the browser
page_to_scrape = webdriver.Chrome(service=browser_driver, options=chrome_options)

try:
    page_to_scrape.get("https://docs.google.com/spreadsheets/d/14V5NBooFYgg144Zsxzgq7E8R9SIA-JhOZynAlssEKoY/edit?usp=sharing")
    time.sleep(2)

    # sip
    page_to_scrape.find_element(By.XPATH, "/html/body/div[4]/div/div[4]/table/tbody/tr[2]/td[3]/div/div[3]/div/div[2]/div/div/div[1]/span").click()
    time.sleep(2) 
    SIP = page_to_scrape.find_element(By.XPATH, '/html/body/div[4]/div/div[2]/div/div[5]/div[2]/div[1]/div[2]')
    SIPtext = SIP.text
    with open("sip_emails.md", "w") as novosti_sip:
        novosti_sip.write(SIPtext)



finally:
    # Close the browser
    page_to_scrape.quit()
