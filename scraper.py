import requests
from bs4 import BeautifulSoup


def store_valid_postings(price, title, link):
    is_valid = check_validity(price, title)
    if is_valid:
        posting = {'price': price, 'title': title, 'link': link}
        valid_postings.append(posting)


def check_validity(price, title):
    is_posting_title_valid = check_keywords(title)
    is_price_valid = check_price(price)
    if is_posting_title_valid and is_price_valid:
        return True
    return False


def check_keywords(title):
    title.lower()
    for keyword in keywords:
        return keyword in title
    return False


def check_price(price):
    if price <= upper_price_limit:
        return True
    return False


search_query = "f30 diffuser"
upper_price_limit = 300
keywords = ['f30', 'f30 diffuser', '328i']

craigslist_URL = 'https://vancouver.craigslist.org/d/for-sale/search/sss?sort=rel&query=f30'

page = requests.get(craigslist_URL)
soup = BeautifulSoup(page.content, 'lxml')
postings = soup.find_all(class_='result-row')

for posting_details in postings:
    price = posting_details.find(class_='result-price').text
    title = posting_details.find('a', class_='result-title').text
    link = posting_details.find('a', class_='result-title')['href']

    # print(title.text)
    print(price)
    # print(link)
    valid_postings = []
    store_valid_postings(price, title, link)
    print(valid_postings)


