from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import requests
from pymongo import MongoClient
from datetime import datetime
import uuid

PROXY = "http://USERNAME:PASSWORD@PROXYMESH_IP:PORT"

def get_driver():
    chrome_options = Options()
    chrome_options.add_argument('--proxy-server=%s' % PROXY)
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def login_to_twitter(driver, username, password):
    driver.get("https://twitter.com/login")
    time.sleep(3)
    username_input = driver.find_element(By.NAME, "session[username_or_email]")
    password_input = driver.find_element(By.NAME, "session[password]")
    username_input.send_keys(username)
    password_input.send_keys(password)
    password_input.send_keys(Keys.RETURN)
    time.sleep(5)  # Wait for the login process to complete

def get_trending_topics(driver):
    driver.get("https://twitter.com/home")
    time.sleep(5)  # Wait for the page to load completely
    trends = driver.find_elements(By.CSS_SELECTOR, "section[aria-labelledby='accessible-list-0'] div[dir='ltr'] span")
    trending_topics = [trend.text for trend in trends[:5]]
    return trending_topics

def fetch_ip_address():
    response = requests.get("https://api.ipify.org?format=json")
    return response.json()["ip"]

def store_to_mongodb(data):
    client = MongoClient("mongodb://localhost:27017/")
    db = client.twitter_trends
    collection = db.trends
    collection.insert_one(data)
    client.close()

def main():
    driver = get_driver()
    username = "YOUR_TWITTER_USERNAME"
    password = "YOUR_TWITTER_PASSWORD"
    login_to_twitter(driver, username, password)
    
    trending_topics = get_trending_topics(driver)
    ip_address = fetch_ip_address()
    unique_id = str(uuid.uuid4())
    end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    data = {
        "_id": unique_id,
        "trend1": trending_topics[0],
        "trend2": trending_topics[1],
        "trend3": trending_topics[2],
        "trend4": trending_topics[3],
        "trend5": trending_topics[4],
        "end_time": end_time,
        "ip_address": ip_address
    }

    store_to_mongodb(data)
    driver.quit()
