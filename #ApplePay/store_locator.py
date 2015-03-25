__author__ = 'Josue Carbonel'

import requests
from bs4 import BeautifulSoup
from unidecode import unidecode
from formating_name_address import print_in_format


def getting_store_list(url):
    """****getting_store_list****
        This method will get the content of the url wanted
        store the name of the store
        and address and then will store it into a list
        every store will be stored in a list so this method will return the list with the:
              Name
              Address"""
    store_list = []
    response = requests.get(url)
    soup = BeautifulSoup(response.content).find_all('div', {'class': 'text-block'})
    soup = str(unidecode(soup[0].text)).split('\n')
    soup = filter(None, soup)

    store_name = soup[0] + ' - ' + soup[4]
    store_name = store_name.replace('Shopping mall:  ', '')
    store_list += [str(store_name)]         # Stores the Name
    store_address = soup[3]
    store_address = store_address.replace('Address: ', '')
    store_list += [str(store_address)]      # Stores the address
    return store_list


def getting_addresses(url):
    """ This method will scrape the web-page and will also
        print the store list in the write format"""
    response = requests.get(url)

    soup = BeautifulSoup(response.content).find_all('div', {'class': 'archive-post-title'})
    for code in soup:
        store_link = BeautifulSoup(str(code)).find_all('a')
        # This will get the link of the store
        store_link = 'http://www.store-locator.info' + store_link[0].get('href')
        # store lists in the format Name and Address
        data = getting_store_list(store_link)
        print_in_format(data)           # Prints it in the right format
