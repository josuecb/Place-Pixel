__author__ = 'Josue Carbonel'

import requests
from bs4 import BeautifulSoup
from unidecode import unidecode
import re
from formating_name_address import print_in_format


def index_parse(my_string):
    """ This will take out every "(text)" there is in our text
        Returning a string without the "(text)" """
    if '[' in my_string:
        my_string = my_string.replace('[', '<')
        if ']' in my_string:
            my_string = my_string.replace(']', '>')

    new_string = re.findall(r'(<.*>)', my_string)
    new_string = ''.join(new_string)

    if new_string[0] in my_string:
        my_string = my_string.replace(new_string, '')
        return my_string


def parse_string_left_overs(my_string):
    """ This removes the extra text it has in our scrapped data
        Deleting "Address:" and "City and Zip Code:" text from out scrapped data"""
    if 'Address:' in my_string:
        my_string = my_string.replace('Address:', '')

    if 'City and Zip Code:' in my_string:
        my_string = my_string.replace('City and Zip Code:', '')

    my_string = my_string.lstrip(' ')
    my_string = my_string.rstrip(' ')

    return my_string


def getting_content(soup):
    """ This will get the code wanted
        Retuning 2 lists: Name list and Address List"""
    # Name code
    name_code = BeautifulSoup(str(soup[0])).find_all('h3', {'itemprop': 'name'})
    # Address code
    address_code = BeautifulSoup(str(soup[0])).find_all('div', {'itemprop': 'address'})

    name_list = []
    for names in name_code:
        names = str(unidecode(names.text))
        names = index_parse(names)
        names = parse_string_left_overs(names)
        name_list += [names]

    address_list = []

    for addresses in address_code:
        # Gets just the address and city
        address = BeautifulSoup(str(addresses)).find_all('div', {'class': 'bs_f'})
        index = 2                                                       # Takes only 2 values
        for address1 in address:
            while index > 0:
                address_values = str(unidecode(address1.text))          # Converts it into a string
                address_values = parse_string_left_overs(address_values)
                address_list += [address_values]
                #print(address_values)
                index -= 1                                              # gets back to 0
                break

    return name_list, address_list


def sorting_content(name_list, address_list):
    """ This will connect our name list and address list into 1 list
        returning a list with the format Name and Address"""
    name_and_address = []
    index_name = len(address_list)/2
    name_index = 0

    index = 0
    while index < len(address_list):
        if name_index == index_name:
            pass
        else:
            name_and_address += [name_list[name_index]]
            index_name += 1

        name_and_address += [address_list[index]]
        index += 1
        name_and_address += [address_list[index]]
        index += 1

    return name_and_address


def scrapping_address(url):
    """ As we have many links the the toy R us site we need to scrape every web-page
        so this method will return a list using sorting content
        and getting content for just 1 link"""
    response = requests.get(url)
    soup = BeautifulSoup(response.content).find_all('div', {'id': 'bs_item_container'})

    name_list, address_list = getting_content(soup)

    name_and_address = sorting_content(name_list, address_list)

    return name_and_address


def unify_lists():
    """ This will use scrapping address to scrape 2 different web sites and will append the
        2 different lists into 1
        returning 1 main list"""
    url = 'http://www.city-data.com/locations/ToysRUs/New-York-New-York.html'
    list1 = scrapping_address(url)
    url = 'http://www.city-data.com/locations/ToysRUs/New-York-New-York-2.html'
    list2 = scrapping_address(url)

    for index in range(0, len(list2)):
        list1 += [list2[index]]

    toy_r_us_file = []

    index = 0
    while index < len(list1):
        toy_r_us_file += [str(list1[index])]
        index += 1
        temp_string = str(list1[index]).lower() + ' '
        index += 1
        toy_r_us_file += [temp_string + str(list1[index])]
        index += 1
    return toy_r_us_file


def print_toy_r_us_stores():
    """ This will just use the main list and will print it in the wanted format using the
        print_in_format method"""
    data = unify_lists()
    print_in_format(data)

