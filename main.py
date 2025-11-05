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

    # sip
    page_to_scrape.get("https://sip.elfak.ni.ac.rs/")
    time.sleep(3)
    responseSIP = page_to_scrape.find_element(By.ID, 'novosti')
    novosti_markdownSIP = responseSIP.text
    with open("sip.md", "w") as novosti_fileSIP:
        novosti_fileSIP.write(novosti_markdownSIP)
    heightSIP = responseSIP.size['height']
    widthSIP = responseSIP.size['width']
    desired_widthSIP = max(widthSIP, 1200)  
    desired_heightSIP = min(heightSIP, 1000)
    page_to_scrape.set_window_size(desired_widthSIP, desired_heightSIP) 
    page_to_scrape.execute_script("arguments[0].scrollIntoView(true);", responseSIP)
    responseSIP.screenshot('sip.png')
    
    # cs elfak login
    page_to_scrape.get("https://cs.elfak.ni.ac.rs/nastava/login/index.php")
    time.sleep(2)
    page_to_scrape.find_element(By.XPATH, "/html/body/div[2]/div[2]/div/div/section/div/div[2]/div/div/div/div/div/div[2]/div[3]/div/a").click()
    time.sleep(2)
    mail = page_to_scrape.find_element(By.XPATH, '//*[@id="i0116"]')
    mail.send_keys(os.environ['MAIL'])  
    page_to_scrape.find_element(By.XPATH, '//*[@id="idSIButton9"]').click()
    time.sleep(2)   
    password = page_to_scrape.find_element(By.XPATH, '//*[@id="i0118"]')
    password.send_keys(os.environ['PASSWORD'])  
    page_to_scrape.find_element(By.XPATH, '//*[@id="idSIButton9"]').click()
    time.sleep(2)
    page_to_scrape.find_element(By.XPATH, '//*[@id="idBtn_Back"]').click()
    time.sleep(2)
    
    # bp
    page_to_scrape.get("https://cs.elfak.ni.ac.rs/nastava/mod/forum/search.php?id=4&words=&phrase=&notwords=&fullwords=&timefromrestrict=1&fromday=1&frommonth=1&fromyear=2025&fromhour=0&fromminute=0&hfromday=0&hfrommonth=0&hfromyear=0&hfromhour=0&hfromminute=0&htoday=1&htomonth=1&htoyear=1&htohour=1&htominute=1&forumid=&subject=&user=")
    time.sleep(3)
    responseBP = page_to_scrape.find_element(By.XPATH, '//*[@id="region-main"]')
    novosti_markdownBP = responseBP.text
    with open("bp.md", "w") as novosti_fileBP:
        novosti_fileBP.write(novosti_markdownBP)
    heightBP = responseBP.size['height']
    widthBP = responseBP.size['width']
    desired_widthBP = max(widthBP, 1200)  
    desired_heightBP = min(heightBP, 1000)
    page_to_scrape.set_window_size(desired_widthBP, desired_heightBP)    
    page_to_scrape.execute_script("arguments[0].scrollIntoView(true);", responseBP)
    responseBP.screenshot('bp.png')

    # oop
    page_to_scrape.get("https://cs.elfak.ni.ac.rs/nastava/mod/forum/search.php?id=45&words=&phrase=&notwords=&fullwords=&timefromrestrict=1&fromday=1&frommonth=9&fromyear=2024&fromhour=0&fromminute=0&hfromday=0&hfrommonth=0&hfromyear=0&hfromhour=0&hfromminute=0&htoday=1&htomonth=1&htoyear=1&htohour=1&htominute=1&forumid=&subject=&user=")
    time.sleep(3)
    responseOOP = page_to_scrape.find_element(By.XPATH, '//*[@id="region-main"]')
    novosti_markdownOOP = responseOOP.text
    with open("oop.md", "w") as novosti_fileOOP:
        novosti_fileOOP.write(novosti_markdownOOP)
    heightOOP = responseOOP.size['height']
    widthOOP = responseOOP.size['width']
    desired_widthOOP = max(widthOOP, 1200)  
    desired_heightOOP = min(heightOOP, 1000)
    page_to_scrape.set_window_size(desired_widthOOP, desired_heightOOP)    
    page_to_scrape.execute_script("arguments[0].scrollIntoView(true);", responseOOP)
    responseOOP.screenshot('oop.png')


    # aor1
    page_to_scrape.get("https://cs.elfak.ni.ac.rs/nastava/mod/forum/search.php?id=139&words=&phrase=&notwords=&fullwords=&timefromrestrict=1&fromday=1&frommonth=1&fromyear=2020&fromhour=0&fromminute=0&hfromday=0&hfrommonth=0&hfromyear=0&hfromhour=0&hfromminute=0&htoday=1&htomonth=1&htoyear=1&htohour=1&htominute=1&forumid=&subject=&user=")
    time.sleep(3)
    responseAOR1 = page_to_scrape.find_element(By.XPATH, '//*[@id="region-main"]')
    novosti_markdownAOR1 = responseAOR1.text
    with open("aor1.md", "w") as novosti_fileAOR1:
        novosti_fileAOR1.write(novosti_markdownAOR1)
    heightAOR1 = responseAOR1.size['height']
    widthAOR1 = responseAOR1.size['width']
    desired_widthAOR1 = max(widthAOR1, 1200)  
    desired_heightAOR1 = min(heightAOR1, 1000)
    page_to_scrape.set_window_size(desired_widthAOR1, desired_heightAOR1)    
    page_to_scrape.execute_script("arguments[0].scrollIntoView(true);", responseAOR1)
    responseAOR1.screenshot('aor1.png')


    # lp
    page_to_scrape.get("https://cs.elfak.ni.ac.rs/nastava/mod/forum/search.php?id=41&words=&phrase=&notwords=&fullwords=&timefromrestrict=1&fromday=1&frommonth=1&fromyear=2025&fromhour=0&fromminute=0&hfromday=0&hfrommonth=0&hfromyear=0&hfromhour=0&hfromminute=0&htoday=1&htomonth=1&htoyear=1&htohour=1&htominute=1&forumid=&subject=&user=")
    time.sleep(3)
    responseLP = page_to_scrape.find_element(By.XPATH, '//*[@id="region-main"]')
    novosti_markdownLP = responseLP.text
    with open("lp.md", "w") as novosti_fileLP:
        novosti_fileLP.write(novosti_markdownLP)
    heightLP = responseLP.size['height']
    widthLP = responseLP.size['width']
    desired_widthLP = max(widthLP, 1200)  
    desired_heightLP = min(heightLP, 1000)
    page_to_scrape.set_window_size(desired_widthLP, desired_heightLP)    
    page_to_scrape.execute_script("arguments[0].scrollIntoView(true);", responseLP)
    responseLP.screenshot('lp.png')

    # oopj
    page_to_scrape.get("https://cs.elfak.ni.ac.rs/nastava/mod/forum/search.php?id=62&words=&phrase=&notwords=&fullwords=&timefromrestrict=1&fromday=1&frommonth=1&fromyear=2025&fromhour=0&fromminute=0&hfromday=0&hfrommonth=0&hfromyear=0&hfromhour=0&hfromminute=0&htoday=1&htomonth=1&htoyear=1&htohour=1&htominute=1&forumid=&subject=&user=")
    time.sleep(3) 
    responseOOPJ = page_to_scrape.find_element(By.XPATH, '//*[@id="region-main"]')
    novosti_markdownOOPJ = responseOOPJ.text
    with open("oopj.md", "w") as novosti_fileOOPJ:
        novosti_fileOOPJ.write(novosti_markdownOOPJ)
    heightOOPJ = responseOOPJ.size['height']
    widthOOPJ = responseOOPJ.size['width']
    desired_widthOOPJ = max(widthOOPJ, 1200)  
    desired_heightOOPJ = min(heightOOPJ, 1000)
    page_to_scrape.set_window_size(desired_widthOOPJ, desired_heightOOPJ)    
    page_to_scrape.execute_script("arguments[0].scrollIntoView(true);", responseOOPJ)
    responseOOPJ.screenshot('oopj.png')

    # sp
    page_to_scrape.get("https://cs.elfak.ni.ac.rs/nastava/mod/forum/search.php?id=9&words=&phrase=&notwords=&fullwords=&timefromrestrict=1&fromday=1&frommonth=1&fromyear=2025&fromhour=0&fromminute=0&hfromday=0&hfrommonth=0&hfromyear=0&hfromhour=0&hfromminute=0&htoday=1&htomonth=1&htoyear=1&htohour=1&htominute=1&forumid=&subject=&user=")
    time.sleep(3)  
    responseSP = page_to_scrape.find_element(By.XPATH, '//*[@id="region-main"]')
    novosti_markdownSP = responseSP.text
    with open("sp.md", "w") as novosti_fileSP:
        novosti_fileSP.write(novosti_markdownSP)
    heightSP = responseSP.size['height']
    widthSP = responseSP.size['width']
    desired_widthSP = max(widthSP, 1200)  
    desired_heightSP = min(heightSP, 1000)
    page_to_scrape.set_window_size(desired_widthSP, desired_heightSP)    
    page_to_scrape.execute_script("arguments[0].scrollIntoView(true);", responseSP)
    responseSP.screenshot('sp.png')

    # pj
    page_to_scrape.get("https://cs.elfak.ni.ac.rs/nastava/mod/forum/search.php?id=11&words=&phrase=&notwords=&fullwords=&timefromrestrict=1&fromday=1&frommonth=1&fromyear=2025&fromhour=0&fromminute=0&hfromday=0&hfrommonth=0&hfromyear=0&hfromhour=0&hfromminute=0&htoday=1&htomonth=1&htoyear=1&htohour=1&htominute=1&forumid=&subject=&user=")
    time.sleep(3) 
    responsePJ = page_to_scrape.find_element(By.XPATH, '//*[@id="region-main"]')
    novosti_markdownPJ = responsePJ.text
    with open("pj.md", "w") as novosti_filePJ:
        novosti_filePJ.write(novosti_markdownPJ)
    heightPJ = responsePJ.size['height']
    widthPJ = responsePJ.size['width']
    desired_widthPJ = max(widthPJ, 1200)  
    desired_heightPJ = min(heightPJ, 1000)
    page_to_scrape.set_window_size(desired_widthPJ, desired_heightPJ)    
    page_to_scrape.execute_script("arguments[0].scrollIntoView(true);", responsePJ)
    responsePJ.screenshot('pj.png')
  
    # dmat
    page_to_scrape.get("https://cs.elfak.ni.ac.rs/nastava/mod/forum/search.php?id=97&words=&phrase=&notwords=&fullwords=&timefromrestrict=1&fromday=1&frommonth=1&fromyear=2025&fromhour=0&fromminute=0&hfromday=0&hfrommonth=0&hfromyear=0&hfromhour=0&hfromminute=0&htoday=1&htomonth=1&htoyear=1&htohour=1&htominute=1&forumid=&subject=&user=")
    time.sleep(3)  
    responseDMAT = page_to_scrape.find_element(By.XPATH, '//*[@id="region-main"]')
    novosti_markdownDMAT = responseDMAT.text
    with open("dmat.md", "w") as novosti_fileDMAT:
        novosti_fileDMAT.write(novosti_markdownDMAT)
    heightDMAT = responseDMAT.size['height']
    widthDMAT = responseDMAT.size['width']
    desired_widthDMAT = max(widthDMAT, 1200)  
    desired_heightDMAT = min(heightDMAT, 1000)
    page_to_scrape.set_window_size(desired_widthDMAT, desired_heightDMAT)    
    page_to_scrape.execute_script("arguments[0].scrollIntoView(true);", responseDMAT)
    responseDMAT.screenshot('dmat.png')

    # aip
    page_to_scrape.get("https://cs.elfak.ni.ac.rs/nastava/mod/forum/search.php?id=3&words=&phrase=&notwords=&fullwords=&timefromrestrict=1&fromday=1&frommonth=1&fromyear=2000&fromhour=0&fromminute=0&hfromday=0&hfrommonth=0&hfromyear=0&hfromhour=0&hfromminute=0&htoday=1&htomonth=1&htoyear=1&htohour=1&htominute=1&forumid=&subject=&user=")
    time.sleep(3)  
    responseAIP = page_to_scrape.find_element(By.XPATH, '//*[@id="region-main"]')
    novosti_markdownAIP = responseAIP.text
    with open("aip.md", "w") as novosti_fileAIP:
        novosti_fileAIP.write(novosti_markdownAIP)
    heightAIP = responseAIP.size['height']
    widthAIP = responseAIP.size['width']
    desired_widthAIP = max(widthAIP, 1200)  
    desired_heightAIP = min(heightAIP, 1000)
    page_to_scrape.set_window_size(desired_widthAIP, desired_heightAIP)    
    page_to_scrape.execute_script("arguments[0].scrollIntoView(true);", responseAIP)
    responseAIP.screenshot('aip.png')

    # uur
    page_to_scrape.get("https://cs.elfak.ni.ac.rs/nastava/mod/forum/search.php?id=2&words=&phrase=&notwords=&fullwords=&timefromrestrict=1&fromday=1&frommonth=1&fromyear=2000&fromhour=0&fromminute=0&hfromday=0&hfrommonth=0&hfromyear=0&hfromhour=0&hfromminute=0&htoday=1&htomonth=1&htoyear=1&htohour=1&htominute=1&forumid=&subject=&user=")
    time.sleep(3)  
    responseUUR = page_to_scrape.find_element(By.XPATH, '//*[@id="region-main"]')
    novosti_markdownUUR = responseUUR.text
    with open("uur.md", "w") as novosti_fileUUR:
        novosti_fileUUR.write(novosti_markdownUUR)
    heightUUR = responseUUR.size['height']
    widthUUR = responseUUR.size['width']
    desired_widthUUR = max(widthUUR, 1200)  
    desired_heightUUR = min(heightUUR, 1000)
    page_to_scrape.set_window_size(desired_widthUUR, desired_heightUUR)    
    page_to_scrape.execute_script("arguments[0].scrollIntoView(true);", responseUUR)
    responseUUR.screenshot('uur.png')


finally:
    # Close the browser
    page_to_scrape.quit()
