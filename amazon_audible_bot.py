from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

options = Options()
options.add_argument("--headless=new")

website = "https://www.audible.com/search"

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get(website)
# driver.maximize_window()

container = driver.find_element('class name', 'adbl-impression-container')
products = container.find_elements('xpath', './/li[contains(@class, "productListItem")]')

book_title = []
book_author = []
book_length = []

for product in products:
   title = product.find_element('xpath', './/h3[contains(@class, "bc-heading")]').text
   book_title.append(title)
   print(title)
   book_author.append(product.find_element('xpath', './/li[contains(@class, "authorLabel")]').text)
   book_length.append(product.find_element('xpath', './/li[contains(@class, "runtimeLabel")]').text)

driver.quit()

df_books = pd.DataFrame({'title': book_title, 'author': book_author, 'length': book_length})
df_books.to_csv('books.csv', index=False)