from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


FORM_URL = "https://forms.gle/iMNDfDiGAX6oMmud6"
ZWILLOW_URL= "https://appbrewery.github.io/Zillow-Clone"

response = requests.get(ZWILLOW_URL)
pattern = r'[+/].*$'

soup = BeautifulSoup(response.text, "html.parser")
all_listings_html = soup.select(".List-c11n-8-84-3-photo-cards .ListItem-c11n-8-84-3-StyledListCardWrapper")
all_listings = [{"url": listing.find(name="a").get("href"), "address": listing.find(name="address").get_text().strip().replace("|",""), "price": re.sub(pattern, '', listing.select_one(".PropertyCardWrapper__StyledPriceLine").text)} for listing in all_listings_html]

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)
driver.get(FORM_URL)



for listing in all_listings:
    
    try:
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='text']")))

        all_inputs = driver.find_elements(By.CSS_SELECTOR, "input[type='text']")
        all_inputs[0].send_keys(listing["url"])
        all_inputs[1].send_keys(listing["price"])
        all_inputs[2].send_keys(listing["address"])
        driver.find_element(By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div').click()
        driver.find_element(By.CSS_SELECTOR, value=".c2gzEf").find_element(By.TAG_NAME, value="a").click()
    except Exception as e:
        print("Timed out waiting for elements or class name is incorrect.")
    
    time.sleep(2)



driver.quit()

