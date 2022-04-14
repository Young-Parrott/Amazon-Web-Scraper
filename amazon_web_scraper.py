from cgitb import text
import csv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

## webdriver instance
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))


## function that inputs search term using string formatting
def get_url(search_term):
    ## Generate a URL
    template = "https://www.amazon.com/s?k={}&crid=2GM7AAQABFGBO&sprefix={}%2Caps%2C98&ref=nb_sb_noss_1"
    search_term = search_term.replace(' ','+')

    ## add term query to url
    url = template.format(search_term, search_term)

    ## add page query placeholder
    url += '&page{}'

    return url

def extract_record(item):
    ## extract and return data froma single record
    # description and url
    atag = item.h2.a.span
    description = atag.text.strip()
    ataglink = item.h2.a
    url = 'https://www.amazon.com' + ataglink.get('href')

    try:
        # price
        ## EDIT THESE LINES IF NOT ABLE TO RETRIEVE PRICE
        price_parent = item.find('span', 'a-price')
        price =price_parent.find('span', 'a-offscreen').text
    except AttributeError:
        return

    try:
        # rank and rating
        ## EDIT THESE LINES IF NOT ABLE TO FIND REVIEW OR REVIEW COUNTS
        rating = item.find('i', {'span', 'a-icon-alt'}).text
        review_count = item.find('a', {'span', 'a-size-base s-underline-text'}).text
    except AttributeError:
        rating = ''
        review_count = ''

    result = (description, price, rating, review_count, url)

    return result

def main(search_term):
    # start the webdriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    records = []
    url = get_url(search_term)

    for page in range(1,20):
        driver.get(url.format(page))
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        ## CHANGE THIS PATH IF YOU CANNOT FIND PRODUCT NAMES
        results = soup.find_all("div", {"class": "a-section a-spacing-base"})

        for item in results:
            record = extract_record(item)
            if record:
                records.append(record)
    driver.close()

    headers = ['Description', 'Price', 'Rating', 'ReviewCount', 'Url']

    with open('results.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(records)


## EDIT THIS TO CHANGE WHAT YOU WANT TO SEARCH FOR
main('Dresser for bedroom')
