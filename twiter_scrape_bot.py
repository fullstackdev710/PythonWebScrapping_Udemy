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

def get_tweet(element):
   try:
      user = element.find_element(By.XPATH, ".//span[contains(text(), '@')]").text
      text = element.find_element(By.XPATH, ".//div[@lang]").text
      tweets_data = [user, text]
   except:
      tweets_data = ['user', 'text']
   return tweets_data

user_data = []
text_data = []
tweet_ids = set()

scrolling = True
while scrolling:
   tweets = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//article[@data-testid='tweet']")))
   for tweet in tweets[-15:]:
      tweet_list = get_tweet(tweet)
      tweet_id = ''.join(tweet_list)
      if tweet_id not in tweet_ids:
         tweet_ids.add(tweet_id)
         user_data.append(tweet_list[0])
         text_data.append(" ".join(tweet_list[0].split()))

   # Infinite scroll
   last_height = driver.execute_script("return document.body.scrollHeight")
   while True:
      driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
      time.sleep(3)
      new_height = driver.execute_script("return document.body.scrollHeight")

      # if new_height == last_height:
      #    scrolling = False
      #    break
      if len(user_data) > 60:
         scrolling = False
         break
      else:
         last_height = new_height
         break

driver.quit()
df_tweets = pd.DataFrame({'user': user_data, 'text': text_data})
df_tweets.to_csv('tweets_infinite_scrolling.csv', index=False)
print(df_tweets)