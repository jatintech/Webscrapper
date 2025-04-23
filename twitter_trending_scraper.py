from selenium import webdriver
from selenium.webdriver import Proxy
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from pymongo import MongoClient
import time
import uuid
import datetime
import json
from webdriver_manager.chrome import ChromeDriverManager

# Optional: Replace this with your own class or dict structure if not using dbobjectClass
class DBObject:
    def __init__(self, _id, timestamp, data):
        self._id = _id
        self.timestamp = timestamp
        self.data = data

def scrape_trending_topics(
    proxy_address=None,
    username="your_username",
    password="your_password",
    mongo_host="localhost",
    mongo_port=27017,
    db_name="twitter",
    collection_name="scrapper"
):
    # Proxy Configuration (if any)
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    if proxy_address:
        prox = Proxy()
        prox.http_proxy = proxy_address
        options.add_argument(f"--proxy-server=http://{proxy_address}")

    # WebDriver Setup
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(10)

    # XPaths
    xpath_username = "//input[@autocomplete='username']"
    xpath_password = "//input[@autocomplete='current-password']"
    xpath_login_btn = "//span[text()='Log in']/ancestor::button"
    xpath_trending = "//div[contains(@aria-label, 'Timeline: Trending now')]//span"

    # Navigate to Twitter login
    driver.get('https://x.com/i/flow/login')
    time.sleep(3)

    # Login process
    driver.find_element(By.XPATH, xpath_username).send_keys(username + Keys.RETURN)
    time.sleep(3)
    driver.find_element(By.XPATH, xpath_password).send_keys(password)
    driver.find_element(By.XPATH, xpath_login_btn).click()
    time.sleep(5)

    # Scrape trending topics
    trending_elements = driver.find_elements(By.XPATH, xpath_trending)
    trends = set()
    for el in trending_elements:
        txt = el.text.strip()
        if txt and not any(keyword in txt for keyword in ["Trending", "posts", "in India", "Show more", "What’s happening"]):
            trends.add(txt)

    # Create DB Object
    db_entry = DBObject(str(uuid.uuid4()), str(datetime.datetime.now()), list(trends))

    # Store in MongoDB
    client = MongoClient(mongo_host, mongo_port)
    collection = client[db_name][collection_name]
    collection.insert_one(db_entry.__dict__)

    # Retrieve all data from DB
    all_entries = list(collection.find())

    # Close browser
    driver.quit()

    return all_entries

# Example usage:
# result = scrape_trending_topics(proxy_address="username:password@proxyserver:port", username="your_username", password="your_password")
