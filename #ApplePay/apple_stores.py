__author__ = 'Josue Carbonel'

from bs4 import BeautifulSoup
import requests
from formating_name_address import print_in_format


# This Method will only return a list with links of all the areas
# that new york has for example: albany, Manhattan, Brooklyn
# to then scrape those links
def apple_store_ny_links():
    url = 'http://www.apple.com/retail/storelist'
    content = requests.get(url)
    soup = BeautifulSoup(content.content)
    us_store_list = soup.find_all('div', {'id': 'usstores'})

    new_york_link = ''
    for us_stores in us_store_list:
        last_column = str(us_stores)
        last_column = BeautifulSoup(last_column).find_all('div', {'class': 'column last'})
        for last_column_only in last_column:
            new_york_region = str(last_column_only)
            new_york_region = BeautifulSoup(new_york_region).find_all('ul')
            for new_york in new_york_region:
                new_york_link = new_york
                break
            break

    new_york_link = BeautifulSoup(str(new_york_link)).find_all('a')
    store_links = []
    for ny_store_links in new_york_link:
        store_link = ny_store_links.get('href')
        store_links += [store_link]

    new_york_store_links = []
    for index in range(0, len(store_links)):
        retail_store = 'http://www.apple.com' + store_links[index]
        new_york_store_links += [retail_store]
    return new_york_store_links


# This parse_category method will help me to scrape a bit more its nothing important
# but will return the code content I need into text
def parse_category(request_variable, code, html_category, type_name):
    soup = BeautifulSoup(request_variable.content).find_all(code, {html_category: type_name})
    soup = soup[0].text
    soup = soup.replace('\n', '')
    soup = soup.replace('\t', '')

    return soup


def print_apple_store_content():
    store_link_list = apple_store_ny_links()  # List of links in ny
    store_link_list = filter(None, store_link_list)

    apple_stores = []
    for index in range(0, len(store_link_list)):
        url = store_link_list[index]  # Using each link
        response = requests.get(url)  # Requesting Content

        name = parse_category(response, 'div', 'class', 'store-name')  # Getting store name
        apple_stores += ['Apple Store - ' + name]  # Complete name
        # Getting address of the store
        address = parse_category(response, 'div', 'class', 'street-address')
        state = parse_category(response, 'span', 'class', 'locality')  # State
        region = parse_category(response, 'span', 'class', 'region')  # Region
        # Postal-code
        postal_code = parse_category(response, 'span', 'class', 'postal-code')
        # Complete Address
        apple_stores += [address + ' ' + state + ', ' + region + ' ' + postal_code]

    # This one uses the code scrapped from the web-page and scrape the name of the store and the address
    # returning a list with:
    # Name
    #       Address
    # You will notice that all the files are made on this format
    print_in_format(apple_stores)  # This will print in the right format
