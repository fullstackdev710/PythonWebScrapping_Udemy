import os
from dotenv import load_dotenv
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

dotenv_path = Path('.env')
load_dotenv(dotenv_path=dotenv_path)

web = 'https://twitter.com/'
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get(web)

login = driver.find_element(By.XPATH, '//a[@href="/login"]')
login.click()
time.sleep(5)

username = driver.find_element(By.XPATH, '//input[@autocomplete ="username"]')
username.send_keys(os.environ.get("TWITTER_USER"))

next_button = driver.find_element(By.XPATH, '//div[@role="button"]//span[text()="Next"]')
next_button.click()
time.sleep(5)

password = driver.find_element(By.XPATH, '//input[@autocomplete ="current-password"]')
password.send_keys(os.environ.get("TWITTER_PASSWORD"))

login_button = driver.find_element(By.XPATH, '//div[@role="button"]//span[text()="Log in"]')
login_button.click()

time.sleep(100)