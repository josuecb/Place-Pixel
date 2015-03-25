__author__ = 'Josue Carbonel'


import requests
from bs4 import BeautifulSoup
from unidecode import unidecode
from formating_name_address import print_in_format


def getting_links(url):
    response = requests.get(url)

    name = BeautifulSoup(response.content).find_all('a', {'class': 'biz-name'})
    address = BeautifulSoup(response.content).find_all('address')
    names = []
    addresses = []
    for each_name in name:
        each_name = each_name.text
        each_name = str(unidecode(each_name))
        names += [each_name]

    for each_address in address:
        each_address = each_address.text
        each_address = str(unidecode(each_address))
        each_address = each_address.replace('\n', '')
        each_address = each_address.replace('\t', '')
        each_address = each_address.lstrip(' ')
        each_address = each_address.rstrip(' ')
        addresses += [each_address]

    page_list = []
    for index in range(0, len(names)):
        if "McDonald" in names[index]:
            page_list += [names[index]]
            page_list += [addresses[index]]

    return page_list


def printing_mcdonals_stores():
    page_index = 0
    while page_index < 1000:
        url = 'http://www.yelp.com/search?find_desc=mcdonals&find_' \
              'loc=New+York%2C+NY&ns=1#start=' + str(page_index)
        data_list = getting_links(url)

        print_in_format(data_list)      # Prints in the format wanted

        page_index += 10
