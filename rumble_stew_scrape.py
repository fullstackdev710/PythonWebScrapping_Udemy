from bs4 import BeautifulSoup
import requests
import shutil
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

root = "https://rumble.com"
website = f"{root}/c/StewPeters"
result = requests.get(website)
content = result.text
soup = BeautifulSoup(content, 'lxml')
root_box = soup.find("div", class_="main-and-sidebar").find('ol')

indexes = [2, 3, 4, 5]
invalid = '<>:"/\|?*'
titles = []

for i in indexes:
   item = root_box.find_all('li', class_="video-listing-entry")[i]
   title = item.find("h3", class_="video-item--title").get_text(strip=True, separator=' ')
   titles.append(title)
   filename = title
   for char in invalid:
      filename = filename.replace(char, '-')
   
   link = item.find('a', class_="video-item--a")['href']
   website = f'{root}{link}'

   driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
   driver.get(website)
   
   box = driver.find_element('id', "videoPlayer").find_element('xpath', '//video[@hidefocus="hidefocus"]')
   
   video_link = box.get_attribute('src')
   img_link = box.get_attribute('poster')

   driver.quit()

   print(video_link)
   print(img_link)

   r = requests.get(img_link, stream=True)
   if r.status_code == 200:
      with open(f'stew_videos/{filename}.jpg', 'wb') as file:
         r.raw.decode_content = True
         shutil.copyfileobj(r.raw, file)

   r = requests.get(video_link, stream=True)
   if r.status_code == 200:
      with open(f'stew_videos/{filename}.mp4', 'wb') as file:
         r.raw.decode_content = True
         shutil.copyfileobj(r.raw, file)


with open(f'stew_videos/title_list.txt', 'w') as file:
   for title in titles:
      file.write(title + '\n\n')

