from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import requests
import time

GOOGLE_FORMS = "https://forms.gle/sy1VqYS6SJEXMk4a8"
RENTING_SITE = "https://appbrewery.github.io/Zillow-Clone/"
Headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36", 
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8,fr;q=0.7", 
}
response = requests.get(url=RENTING_SITE, headers=Headers)

soup = BeautifulSoup(response.text, "html.parser")
price = soup.find_all(name="span", class_="PropertyCardWrapper__StyledPriceLine")
prices =  [p.getText().replace("/mo","").split("+")[0] for p in price if "$" in p.text]
# print(prices)

address = soup.select(".StyledPropertyCardDataArea-anchor address")
addresses = [add.getText().replace("|", "").strip() for add in address]
# print(addresses)

link = soup.find_all(name="a", class_="property-card-link")
links = [l.get("href") for l in link]
# print(links)

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)


for i in range(len(links)):
    time.sleep(3)
    driver.get(url=GOOGLE_FORMS)
    address_google = driver.find_element(by=By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    address_google.send_keys(addresses[i])
    
    price_google = driver.find_element(by=By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price_google.send_keys(prices[i])
    
    link_google = driver.find_element(by=By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link_google.send_keys(links[i])
    
    submit = driver.find_element(by=By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span')
    submit.click()
    
    
driver.quit()