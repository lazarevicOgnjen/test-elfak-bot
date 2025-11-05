from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

# Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920,1080")

# Use Chrome from the setup-chrome action
chrome_options.binary_location = "/usr/bin/google-chrome"

# Chrome driver setup - use the one installed by setup-chrome
browser_driver = Service('/usr/bin/chromedriver')

# Start the browser
driver = webdriver.Chrome(service=browser_driver, options=chrome_options)
wait = WebDriverWait(driver, 10)

def save_content_and_screenshot(url, xpath, md_filename, png_filename):
    """Navigate to a URL, extract text, and take a screenshot."""
    driver.get(url)
    element = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
    
    # Save text to markdown
    with open(md_filename, "w") as f:
        f.write(element.text)
    
    # Adjust window size for screenshot
    width = max(element.size['width'], 1200)
    height = min(element.size['height'], 1000)
    driver.set_window_size(width, height)
    driver.execute_script("arguments[0].scrollIntoView(true);", element)
    element.screenshot(png_filename)

try:
    # SIP page
    save_content_and_screenshot(
        "https://sip.elfak.ni.ac.rs/",
        '//*[@id="novosti"]',
        "sip.md",
        "sip.png"
    )

    # Login to CS
    driver.get("https://cs.elfak.ni.ac.rs/nastava/login/index.php")
    wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[2]/div/div/section/div/div[2]/div/div/div/div/div/div[2]/div[3]/div/a"))).click()
    mail = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="i0116"]')))
    mail.send_keys(os.environ['MAIL'])
    driver.find_element(By.XPATH, '//*[@id="idSIButton9"]').click()
    password = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="i0118"]')))
    password.send_keys(os.environ['PASSWORD'])
    driver.find_element(By.XPATH, '//*[@id="idSIButton9"]').click()
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="idBtn_Back"]'))).click()

    # List of forum pages to scrape
    forum_pages = [
        ("bp", "https://cs.elfak.ni.ac.rs/nastava/mod/forum/search.php?id=4&words=&phrase=&notwords=&fullwords=&timefromrestrict=1&fromday=1&frommonth=1&fromyear=2023&fromhour=0&fromminute=0&hfromday=0&hfrommonth=0&hfromyear=0&hfromhour=0&hfromminute=0&htoday=1&htomonth=1&htoyear=1&htohour=1&htominute=1&forumid=&subject=&user="),
        ("oop", "https://cs.elfak.ni.ac.rs/nastava/mod/forum/search.php?id=45&words=&phrase=&notwords=&fullwords=&timefromrestrict=1&fromday=1&frommonth=1&fromyear=2023&fromhour=0&fromminute=0&hfromday=0&hfrommonth=0&hfromyear=0&hfromhour=0&hfromminute=0&htoday=1&htomonth=1&htoyear=1&htohour=1&htominute=1&forumid=&subject=&user="),
        ("aor1", "https://cs.elfak.ni.ac.rs/nastava/mod/forum/search.php?id=139&words=&phrase=&notwords=&fullwords=&timefromrestrict=1&fromday=1&frommonth=1&fromyear=2020&fromhour=0&fromminute=0&hfromday=0&hfrommonth=0&hfromyear=0&hfromhour=0&hfromminute=0&htoday=1&htomonth=1&htoyear=1&htohour=1&htominute=1&forumid=&subject=&user="),
        ("lp", "https://cs.elfak.ni.ac.rs/nastava/mod/forum/search.php?id=41&words=&phrase=&notwords=&fullwords=&timefromrestrict=1&fromday=1&frommonth=1&fromyear=2023&fromhour=0&fromminute=0&hfromday=0&hfrommonth=0&hfromyear=0&hfromhour=0&hfromminute=0&htoday=1&htomonth=1&htoyear=1&htohour=1&htominute=1&forumid=&subject=&user="),
        ("sp", "https://cs.elfak.ni.ac.rs/nastava/mod/forum/search.php?id=9&words=&phrase=&notwords=&fullwords=&timefromrestrict=1&fromday=1&frommonth=1&fromyear=2023&fromhour=0&fromminute=0&hfromday=0&hfrommonth=0&hfromyear=0&hfromhour=0&hfromminute=0&htoday=1&htomonth=1&htoyear=1&htohour=1&htominute=1&forumid=&subject=&user="),
        ("oopj", "https://cs.elfak.ni.ac.rs/nastava/mod/forum/search.php?id=62&words=&phrase=&notwords=&fullwords=&timefromrestrict=1&fromday=1&frommonth=1&fromyear=2023&fromhour=0&fromminute=0&hfromday=0&hfrommonth=0&hfromyear=0&hfromhour=0&hfromminute=0&htoday=1&htomonth=1&htoyear=1&htohour=1&htominute=1&forumid=&subject=&user="),
        ("dmat", "https://cs.elfak.ni.ac.rs/nastava/mod/forum/search.php?id=97&words=&phrase=&notwords=&fullwords=&timefromrestrict=1&fromday=1&frommonth=1&fromyear=2023&fromhour=0&fromminute=0&hfromday=0&hfrommonth=0&hfromyear=0&hfromhour=0&hfromminute=0&htoday=1&htomonth=1&htoyear=1&htohour=1&htominute=1&forumid=&subject=&user="),
        ("pj", "https://cs.elfak.ni.ac.rs/nastava/mod/forum/search.php?id=11&words=&phrase=&notwords=&fullwords=&timefromrestrict=1&fromday=1&frommonth=1&fromyear=2023&fromhour=0&fromminute=0&hfromday=0&hfrommonth=0&hfromyear=0&hfromhour=0&hfromminute=0&htoday=1&htomonth=1&htoyear=1&htohour=1&htominute=1&forumid=&subject=&user="),
        ("aip", "https://cs.elfak.ni.ac.rs/nastava/mod/forum/search.php?id=3&words=&phrase=&notwords=&fullwords=&timefromrestrict=1&fromday=1&frommonth=1&fromyear=2023&fromhour=0&fromminute=0&hfromday=0&hfrommonth=0&hfromyear=0&hfromhour=0&hfromminute=0&htoday=1&htomonth=1&htoyear=1&htohour=1&htominute=1&forumid=&subject=&user="),
        ("uur", "https://cs.elfak.ni.ac.rs/nastava/mod/forum/search.php?id=2&words=&phrase=&notwords=&fullwords=&timefromrestrict=1&fromday=1&frommonth=1&fromyear=2023&fromhour=0&fromminute=0&hfromday=0&hfrommonth=0&hfromyear=0&hfromhour=0&hfromminute=0&htoday=1&htomonth=1&htoyear=1&htohour=1&htominute=1&forumid=&subject=&user=")
    ]

    for name, url in forum_pages:
        save_content_and_screenshot(url, '//*[@id="region-main"]', f"{name}.md", f"{name}.png")

finally:
    driver.quit()
