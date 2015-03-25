__author__ = 'Josue Carbonel'

import requests
from bs4 import BeautifulSoup
from unidecode import unidecode
from formating_name_address import print_in_format


def getting_area_url():
    """ This Method will only return a list with links of all the areas
        that new york has for example: albany, Manhattan, Brooklyn
        to then scrape those links"""
    url = 'http://www.bjs.com/webapp/wcs/stores/servlet/LocatorAllClubsView?langId=-' \
          '1&storeId=10201&catalogId=10201'
    response = requests.get(url)
    soup = BeautifulSoup(response.content).find_all('td', {'width': '25%'})
    #print(soup)

    wanted_column = ''
    column = 0
    for columns in soup:
        if column == 2:
            wanted_column = columns
            break
        else:
            column += 1

    get_new_york_code = BeautifulSoup(str(wanted_column)).find_all('li')

    places_list = []
    flag_index = 0
    for places in get_new_york_code:
        new_text = BeautifulSoup(str(places)).text

        if flag_index > 0:
            places_list += [places]
        new_york = "New York"

        if new_york == new_text:
            flag_index = 1

    #print(places_list)
    store_info_url = []
    bjs_stores_links = []
    for index in range(0, len(places_list)):
        store_info_url += BeautifulSoup(str(places_list[index])).find_all('a')
        store_info_url[index] = store_info_url[index].get('href')
        store_info_url[index] = 'http://www.bjs.com' + store_info_url[index]
        bjs_stores_links += [str(store_info_url[index])]

    return bjs_stores_links


def bjs_stores_data_list(url):
    """ This will scrape each area link and store the name of the store
        and address and then will store it into a list
        every store will be stored in a list so this method will return the list with the:
              Name
              Address"""
    bjs_stores = []
    response = requests.get(url)
    soup = BeautifulSoup(response.content).find_all('div', {'itemprop': 'address'})
    soup_text = unidecode(soup[0].text)
    soup_text = soup_text.replace('\t', '').replace('\r', '')
    soup_text = soup_text.split('\n')
    soup_text = filter(None, soup_text)
    name = soup_text[0]
    street = soup_text[1]
    region = soup_text[2]
    state = soup_text[3]
    zip_code = soup_text[4]
    region_state_zip = region + state + zip_code

    bjs_stores += ["Bj's - " + name]                    # Name
    bjs_stores += [street + ' ' + region_state_zip]     # Address

    return bjs_stores


def print_bjs_stores():
    area_links = getting_area_url()
    area_links = filter(None, area_links)

    for index in range(0, len(area_links)):
        store_list = bjs_stores_data_list(area_links[index])
        print_in_format(store_list)
