from bs4 import BeautifulSoup
import requests

root = "https://subslikescript.com"
website = f"{root}/movies_letter-A"
result = requests.get(website)
content = result.text
soup = BeautifulSoup(content, 'lxml')

pagination = soup.find('ul', class_='pagination')
pages = pagination.find_all('li', class_='page-item')
last_page = pages[-2].text

for page in range(1, int(last_page)+1):
   website = f"{root}/movies_letter-A?page={page}"
   result = requests.get(website)
   content = result.text
   soup = BeautifulSoup(content, 'lxml')

   box = soup.find('article',class_='main-article')

   links = []
   for link in box.find_all('a', href=True):
      links.append(link['href'])

   invalid = '<>:"/\|?*'

   for link in links:
      try:
         website = f"{root}/{link}"
         result = requests.get(website)
         content = result.text
         soup = BeautifulSoup(content, 'lxml')
         box = soup.find('article',class_='main-article')
         title = box.find('h1').get_text(strip=True, separator=' ')
         filename = title

         for char in invalid:
            filename = filename.replace(char, '-')

         transcript = box.find('div', class_='full-script').get_text(strip=True, separator=' ')
      except:
         print('-------Link not working ----------------')
         print(link)

      with open(f'movies/{filename}.txt','w', encoding="utf-8") as file:
         file.write(title)
         file.write(transcript)

