from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, NoSuchElementException
import os
import time

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
wait = WebDriverWait(driver, 20)  # Increased wait time

def save_content_and_screenshot(url, xpath, md_filename, png_filename):
    """Navigate to a URL, extract text, and take a screenshot."""
    try:
        driver.get(url)
        element = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        
        # Get the text content
        content = element.text
        print(f"Scraped {len(content)} characters for {md_filename}")
        
        # Save text to markdown
        with open(md_filename, "w", encoding='utf-8') as f:
            f.write(content)
        
        print(f"Saved content to {md_filename}")
        
        # Adjust window size for screenshot
        width = max(element.size['width'], 1200)
        height = min(element.size['height'], 1000)
        driver.set_window_size(width, height)
        driver.execute_script("arguments[0].scrollIntoView(true);", element)
        element.screenshot(png_filename)
        print(f"Saved screenshot to {png_filename}")
        
    except Exception as e:
        print(f"Error in save_content_and_screenshot for {md_filename}: {e}")
        raise

def login_to_cs():
    """Handle the login process with robust error handling and fresh element lookups"""
    try:
        print("Starting login process...")
        
        # Navigate to login page
        driver.get("https://cs.elfak.ni.ac.rs/nastava/login/index.php")
        print("Loaded login page")
        
        # Click on Office 365 login with retry
        max_retries = 3
        for attempt in range(max_retries):
            try:
                office365_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[2]/div/div/section/div/div[2]/div/div/div/div/div/div[2]/div[3]/div/a")))
                office365_btn.click()
                print("Clicked Office 365 login")
                break
            except StaleElementReferenceException:
                if attempt < max_retries - 1:
                    print(f"Stale element on Office 365 button, retrying... ({attempt + 1}/{max_retries})")
                    time.sleep(2)
                else:
                    raise
        
        # Wait for email field and enter email
        mail_field = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="i0116"]')))
        mail_field.clear()
        mail_field.send_keys(os.environ['MAIL'])
        print("Entered email")
        
        # Click next button with fresh lookup
        next_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="idSIButton9"]')))
        next_btn.click()
        print("Clicked next button")
        
        # Wait for password field - allow time for page transition
        time.sleep(3)
        password_field = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="i0118"]')))
        password_field.clear()
        password_field.send_keys(os.environ['PASSWORD'])
        print("Entered password")
        
        # Click sign in button with fresh lookup
        signin_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="idSIButton9"]')))
        signin_btn.click()
        print("Clicked sign in button")
        
        # Handle "Stay signed in" prompt if it appears
        try:
            no_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="idBtn_Back"]'))
            )
            no_btn.click()
            print("Clicked 'No' on stay signed in prompt")
        except TimeoutException:
            print("No 'Stay signed in' prompt appeared")
        
        # Wait for login to complete by checking for CS navigation or dashboard
        print("Waiting for login to complete...")
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@class, "breadcrumb") or contains(@class, "navbar") or contains(@class, "dashboard")]')))
        print("Successfully logged in to CS")
        
        # Additional verification - check if we're actually logged in
        current_url = driver.current_url
        if "login" in current_url.lower():
            raise Exception("Still on login page after login attempt")
            
        print(f"Landed on: {current_url}")
        
    except Exception as e:
        print(f"Login failed: {e}")
        # Take screenshot for debugging
        driver.save_screenshot("login_error.png")
        print("Saved login_error.png for debugging")
        raise

def safe_scrape_courses():
    """Scrape courses with individual error handling"""
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

    successful_scrapes = 0
    for name, url in forum_pages:
        try:
            print(f"Scraping {name}...")
            save_content_and_screenshot(url, '//*[@id="region-main"]', f"{name}.md", f"{name}.png")
            print(f"✅ Successfully scraped {name}")
            successful_scrapes += 1
        except Exception as e:
            print(f"❌ Failed to scrape {name}: {e}")
            # Continue with other courses even if one fails
            continue
    
    print(f"Scraping completed: {successful_scrapes}/{len(forum_pages)} courses successful")

try:
    # SIP page (no login required)
    print("Starting SIP page scrape...")
    save_content_and_screenshot(
        "https://sip.elfak.ni.ac.rs/",
        '//*[@id="novosti"]',
        "sip.md",
        "sip.png"
    )
    print("✅ SIP page completed")

    # Login to CS
    print("Starting CS login...")
    login_to_cs()

    # Scrape all courses
    print("Starting course scraping...")
    safe_scrape_courses()

    print("🎉 All tasks completed successfully!")

except Exception as e:
    print(f"❌ Script failed: {e}")
    # Save final screenshot for debugging
    driver.save_screenshot("final_error.png")
    raise

finally:
    driver.quit()
    print("Browser closed")
