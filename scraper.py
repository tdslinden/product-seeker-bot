import requests
from bs4 import BeautifulSoup

search_query = "f30 diffuser"
upper_price_limit = 300
keywords = ['f30', 'f30 diffuser', '328i']

craigslist_URL = 'https://vancouver.craigslist.org/d/for-sale/search/sss?sort=rel&query=f30'

page = requests.get(craigslist_URL)
soup = BeautifulSoup(page.content, 'lxml')
postings = soup.find_all(class_='result-row')

for posting_details in postings:
    price = posting_details.find(class_='result-price').text
    title = posting_details.find('a', class_='result-title')
    link = posting_details.find('a', class_='result-title')['href']

    print(title.text)
    print(price)
    print(link)







