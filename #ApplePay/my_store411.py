__author__ = 'Josue Carbonel'


import requests
from bs4 import BeautifulSoup
from unidecode import unidecode


def get_url_code(url):
    """ This Code gets the URL code"""
    response = requests.get(url)
    soup = BeautifulSoup(response.content).find_all('tr')

    location_in_ny = []
    copy = False
    for tr_code in soup:
        tr_code = str(tr_code)
        if 'Roosevelt' in tr_code:          # Beginning
            copy = True
        if copy is True:
            location_in_ny += [tr_code]
        if '914-684-6300' in tr_code:       # End
            break

    return location_in_ny


def get_link_area_content(store_link):
    """ This method will get the link of all new york area from the main link"""
    response = requests.get(store_link)
    soup = BeautifulSoup(response.content).find_all('div', {'class': 'store-details'})
    for content in soup:
        content = unidecode(content.text).split('\n')
        content = filter(None, content)
        address = content[2].lstrip(' ')
        address = address.rstrip(' ')
        return address          # It will just get one


def getting_store_list(url):
    """ This will return a list with the name and address"""
    location_in_ny = get_url_code(url)

    bloomingdales_stores = []
    for index in range(0, len(location_in_ny)):
        store_name = BeautifulSoup(location_in_ny[index]).find_all('a')
        store_name = str(unidecode(store_name[0].text))
        store_link = BeautifulSoup(location_in_ny[index]).find_all('a')
        store_link = 'http://mystore411.com' + store_link[0].get('href')
        store_link = store_link.replace("'", '%27')

        bloomingdales_stores += [store_name]                # Stores Name
        store_address = get_link_area_content(store_link)   # Gets the store address from the link
        bloomingdales_stores += [store_address]             # Stores Address

    return bloomingdales_stores





