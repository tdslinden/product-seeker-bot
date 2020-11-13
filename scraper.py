import requests
from bs4 import BeautifulSoup


def number_of_pages(total_postings):
    total_postings_num = int(total_postings)
    postings_in_page = 120
    pages = total_postings_num / postings_in_page
    return pages


def store_valid_postings(price, title, link):
    is_valid = check_validity(price, title)
    if is_valid:
        posting = {'title': title, 'price': price, 'link': link}
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
        if keyword in title:
            return True
    return False


def format_price(price):
    converted_price = price
    if price.find(',') != -1:
        converted_price = price.replace(',', '')
    return int(converted_price[1:])


def check_price(price):
    formatted_price = format_price(price)
    if formatted_price <= upper_price_limit:
        return True
    return False


search_query = "f30"
upper_price_limit = 300
keywords = ['f30', 'f30 diffuser', '328i']

craigslist_URL = 'https://vancouver.craigslist.org/d/for-sale/search/sss?sort=rel&query=f30'

page = requests.get(craigslist_URL)
soup = BeautifulSoup(page.content, 'lxml')
total_postings = soup.find(class_='totalcount').text
pages = number_of_pages(total_postings)
postings = soup.find_all(class_='result-row')
valid_postings = []

for posting_details in postings:
    price = posting_details.find(class_='result-price').text
    title = posting_details.find('a', class_='result-title').text
    link = posting_details.find('a', class_='result-title')['href']
    store_valid_postings(price, title, link)

print(valid_postings)
