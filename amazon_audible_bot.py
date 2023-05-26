from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

options = Options()
# options.add_argument("--headless=new")

website = "https://www.audible.com/adblbestsellers?ref=a_search_t1_navTop_pl0cg1c0r0&pf_rd_p=8a113f1a-dc38-418d-b671-3cca04245da5&pf_rd_r=899128M9FDYD7HQ368E3&pageLoadId=LSigJBhQMv1rPgui&creativeId=1642b4d1-12f3-4375-98fa-4938afc1cedc"

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get(website)
driver.maximize_window()

# pagination
pagination = driver.find_element('xpath', '//ul[contains(@class, "pagingElements")]')
pages = pagination.find_elements(By.TAG_NAME, 'li')
last_page = int(pages[-2].text)

current_page = 1

book_title = []
book_author = []
book_length = []

while current_page <= last_page:
   time.sleep(2)
   container = driver.find_element('class name', 'adbl-impression-container')
   products = container.find_elements('xpath', './/li[contains(@class, "productListItem")]')

   for product in products:
      title = product.find_element('xpath', './/h3[contains(@class, "bc-heading")]').text
      book_title.append(title)
      print(title)
      book_author.append(product.find_element('xpath', './/li[contains(@class, "authorLabel")]').text)
      book_length.append(product.find_element('xpath', './/li[contains(@class, "runtimeLabel")]').text)

   current_page = current_page + 1

   try:
      next_page = driver.find_element('xpath', '//span[contains(@class, "nextButton")]')
      next_page.click()
   except:
      pass

driver.quit()

df_books = pd.DataFrame({'title': book_title, 'author': book_author, 'length': book_length})
df_books.to_csv('books.csv', index=False)