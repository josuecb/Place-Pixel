__author__ = 'Josue Carbonel'


import requests
from lxml.html import fromstring
from bs4 import BeautifulSoup
from unidecode import unidecode
from formating_name_address import print_in_format


def getting_url_code():
    """***getting_url_code***
        What it basically does is submit a post with the state it wants to scrape
        because this page is javascript based so that it will return the wanted page code"""
    session = requests.Session()
    url = 'http://www.aeropostale.com/storeLocator/index.jsp'
    response = session.get(url)

    html = fromstring(response.content)
    payload = dict(html.forms[2].fields)
    payload.update(({'searchType': 'STATE', 'state': 'NY', 'radius': '50'}))
    #print(payload)
    locations = session.post('http://www.aeropostale.com/storeLocator/results.jsp', data=payload)
    source_code = BeautifulSoup(locations.content)
    return source_code


def get_aeropostale_list():
    """ This one uses the code scrapped from the web-page and scrape the name of the store
        and the address returning a list with:
              Name
              Address
        You will notice that all the files are made on this format"""
    my_code = getting_url_code()
    my_code = my_code.find_all('table', {'cellspacing': '0'})
    td_code = BeautifulSoup(str(my_code[0])).find_all('td')

    content_list = []
    for td_content in td_code:
        td_content = unidecode(td_content.text).replace('\t', '')
        #td_content = td_content.replace('\t', '')
        content_list += [td_content]
        #print(td_content)

    # This list is getting 3 elements (name & phone, address, maps & direction)
    #print(content_list)
    # We are going to get the address here
    address_list = []
    flag_index = 1
    for index in range(0, len(content_list)):
        if index == flag_index:
            address_list += [content_list[index]]
            flag_index += 3
    # We have the whole address list we have to have 44 addresses
    #print(address_list)
    # print(len(address_list)       #  Yeah we have 44 addresses

    get_data = []
    for index in range(0, len(address_list)):
        address_list[index] = address_list[index].split('\n')
        address_list[index] = filter(None, address_list[index])
        name = address_list[index][0]
        street = address_list[index][1]
        state_zip = address_list[index][2]

        get_data += ['Aeropostal - ' + name]
        get_data += [street + ' ' + state_zip]

    return get_data


def print_aeropostale_stores():
    data_list = get_aeropostale_list()
    print_in_format(data_list)
