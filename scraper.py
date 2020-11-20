import requests
import db_util
import smtplib
import yaml
from bs4 import BeautifulSoup
from datetime import datetime
from email.message import EmailMessage


def number_of_pages(total_postings):
    total_postings_num = int(total_postings)
    postings_in_page = 120
    pages = total_postings_num / postings_in_page
    pages = pages + 1  # add one for the current page
    return int(pages)


def store_valid_postings(pid, price, title, link):
    is_valid = check_validity(pid, price, title)
    pid = int(pid)
    if is_valid:
        posting = {'pid': pid, 'title': title, 'price': price, 'link': link}
        valid_postings.append(posting)
        insert_into_database(pid, title, price, link)


def check_validity(pid, price, title):
    is_pid_valid = check_pid(pid)
    is_posting_title_valid = check_keywords(title)
    is_price_valid = check_price(price)
    if is_posting_title_valid and is_price_valid and is_pid_valid:
        return True
    return False


def check_pid(pid):
    query = 'SELECT * from Postings where pid = ?'
    cursor = get_database().cursor()
    cursor.execute(query, (pid,))
    records = cursor.fetchone()

    if records is None:
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


def parse_next_page(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'lxml')
    postings = soup.find_all(class_='result-row')
    return postings


def get_database():
    conn = db_util.create_connection()
    return conn


def insert_into_database(pid, title, price, link):
    entry_date = datetime.now()
    query = ''' INSERT INTO Postings (pid, title, price, link, entry_date) VALUES (?,?,?,?,?) '''
    conn = get_database()
    cursor = conn.cursor()
    posting_record = (pid, title, price, link, entry_date)
    cursor.execute(query, posting_record)
    conn.commit()
    conn.close()


def remove_outdated_postings():
    has_postings = check_if_postings_exist()
    if has_postings:
        query = "DELETE FROM Postings WHERE entry_date <= datetime('now', '-15 day')"
        conn = get_database()
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()


def check_if_postings_exist():
    query = 'SELECT * from Postings'
    cursor = get_database().cursor()
    cursor.execute(query)
    records = cursor.fetchone()
    if records is None:
        return False
    return True


def send_alerts(body, to):
    credentials_yaml = 'credentials.yaml'
    credentials = read_parameters_from_yaml(credentials_yaml)
    message = EmailMessage()
    message.set_content(body)
    message['subject'] = 'New Postings'
    message['to'] = to

    user = credentials['user']
    message['from'] = user
    password = credentials['password']

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(user, password)
    server.send_message(message)

    server.quit()


def format_message(postings):
    message = ''
    for posting in postings:
        message += posting['title'] + ' ' + posting['link'] + '\n \n'
    return message


def read_parameters_from_yaml(filename):
    with open(filename) as file:
        params = yaml.load(file, Loader=yaml.FullLoader)
        return params


parameters_yaml = 'parameters.yaml'
params = read_parameters_from_yaml(parameters_yaml)
search_query = params['search_query']
keywords = params['keywords']
upper_price_limit = params['upper_limit_price']
to = params['email']

craigslist_url = 'https://vancouver.craigslist.org/d/for-sale/search/sss?sort=rel&query={}'.format(search_query)

page = requests.get(craigslist_url)
soup = BeautifulSoup(page.content, 'lxml')
postings_count = soup.find(class_='totalcount').text
pages = number_of_pages(postings_count)
postings = soup.find_all(class_='result-row')
craigslist_url_with_pages = craigslist_url + '&s={}'
valid_postings = []
remove_outdated_postings()
for i in range(pages):
    for posting_details in postings:
        pid = posting_details['data-pid']
        price = posting_details.find(class_='result-price').text
        title = posting_details.find('a', class_='result-title').text
        link = posting_details.find('a', class_='result-title')['href']
        store_valid_postings(pid, price, title, link)

    current_postings_count = 120 * (i + 1)
    url = craigslist_url_with_pages.format(str(current_postings_count))
    postings = parse_next_page(url)

message = format_message(valid_postings)
if message:
    send_alerts(message, to)

for postings in valid_postings:
    print(postings)
