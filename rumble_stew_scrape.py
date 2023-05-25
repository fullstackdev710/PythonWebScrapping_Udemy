from bs4 import BeautifulSoup
import requests
import shutil

root = "https://rumble.com"
website = f"{root}/c/StewPeters"
result = requests.get(website)
content = result.text
soup = BeautifulSoup(content, 'lxml')
box = soup.find("div", class_="main-and-sidebar").find('ol')

indexes = [1, 2, 3, 4]
invalid = '<>:"/\|?*'

for i in indexes:
   item = box.find_all('li', class_="video-listing-entry")[i]
   title = item.find("h3", class_="video-item--title").get_text(strip=True, separator=' ')
   filename = title
   for char in invalid:
      filename = filename.replace(char, '-')
   
   link = item.find('a', class_="video-item--a")['href']
   website = f'{root}{link}'
   result = requests.get(website)
   content = result.text
   soup = BeautifulSoup(content, 'lxml')
   print(soup.prettify())
   box = soup.find('div', id="videoPlayer")
   
   video_link = box.find_all('video')[0]['src']
   img_link = box.find_all('video')[0]['poster']

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

   # print(title)
   # print((filename))
   # print(img_link)

