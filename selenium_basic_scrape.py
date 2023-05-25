from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

website = 'https://www.adamchoi.co.uk/overs/detailed'

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get(website)

all_matches_button = driver.find_element('xpath', '//label[@analytics-event="All matches"]')
all_matches_button.click()

dropdown = Select((driver.find_element('id', 'country')))
dropdown.select_by_visible_text('Spain')
time.sleep(3)


matches = driver.find_elements('tag name', 'tr')

date = []
home_team = []
score = []
away_team = []

for match in matches:
   date.append(match.find_element('xpath', './td[1]').text)
   home = match.find_element('xpath', './td[2]').text
   home_team.append(home)
   score.append(match.find_element('xpath', './td[3]').text)
   away_team.append(match.find_element('xpath', './td[4]').text)
   print(home)

driver.quit()

df = pd.DataFrame({'date': date, 'home_team': home_team, 'score': score, 'away_team': away_team})
df.to_csv('football_data.csv', index=False)
print(df)