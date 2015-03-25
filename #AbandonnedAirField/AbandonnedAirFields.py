__author__ = 'Josue Carbonel'

import requests
from bs4 import BeautifulSoup
import os
from unidecode import *
import re

# This is The url for all states: http://www.airfields-freeman.com/ and use the function get_all_states
# get_all_states(url, file_name)

# If you just one for 1 state you have to put the state link and the state acronym, e.i: 'NY'
# For example for new york only: http://www.airfields-freeman.com/NY/Airfields_NY.htm
# and use the Function get get_region_data(url, state, file_name, default_file_name)


def state_airfields_url(url, state=None, all_states=None):
    response = requests.get(url)
    soup = BeautifulSoup(response.content).find_all('table')

    soup = BeautifulSoup(str(soup[0])).find_all('a')

    airfields_links = []
    for content in soup:
        if all_states is True:
            content = 'http://www.airfields-freeman.com/' + content.get('href')
        else:
            content = 'http://www.airfields-freeman.com/' + state + '/' + content.get('href')
        airfields_links += [content]
        #print(content)

    return airfields_links


def get_airfield_address(airfield_link, address_list, state):
    response = requests.get(airfield_link)
    soup = BeautifulSoup(response.content).find_all('p')

    find_state = ', ' + state
    temp_soup = soup
    for index in range(0, len(soup)):
        if find_state in str(soup[index]):              # It will find if there is the state in the title
            if 'sans-serif' in str(soup[index]):        # This is the code that has to have the title
                # Temp soup + 1 is the the supposed address if there are coordinates it means
                # that the previous is the correct name and not junk text
                coordinates = re.findall(r'\d+\.\d+', str(temp_soup[index + 1]))

                if len(coordinates) > 0:
                    if coordinates[0] in str(temp_soup[index + 1]):     # Checks if there is coordinates in the address
                        name = str(unidecode(soup[index].text)).replace('\r', ' ')
                        name = name.replace('\n', '')
                        address_list += [name]
                        address = str(unidecode(temp_soup[index + 1].text)).replace('\r', ' ')
                        address = address.replace('\n', '')
                        address_list += [address]
                        #print (str(unidecode(soup[index].text)))
                        #print (str(unidecode(temp_soup[index + 1].text)))
                else:       # In case there is not coordinates in the text
                    pass


def write_file_from_list(file_name, address_list):
    airfield_file = open(file_name, 'a')

    index = 0
    while index < len(address_list):
        airfield_file.write(str(address_list[index]) + '\n')
        index += 1
        airfield_file.write(str(address_list[index]) + '\n\n')
        index += 1
    airfield_file.close()


#   '''''get_region_data(url, state, file_name, default_file_name)''''
#   This method is used like this:
#           You don't need to put a file_name
#           if you don't want to but it will gives you a file with a default name for your
#           file if you set default_file_name as True
#
#           If you don't want to get any text file then do not set any value for
#           default_file_name variable and file_name variables as well
#
#           If you set the variable file_name a value it will return a text file with all the data and the
#           file name wanted therefore you don't have to use the default_file_name variable
def get_region_data(url, state, file_name=None, default_file_name=None):
    try:
        region_links = state_airfields_url(url, state)
        #print(region_links)
    except:
        region_links = [url]

    name_and_addresses_list = []
    for index in range(0, len(region_links)):
        get_airfield_address(region_links[index], name_and_addresses_list, state)

    #print(name_and_addresses_list)

    if file_name is not None:
        write_file_from_list(file_name, name_and_addresses_list)
    else:
        if default_file_name is True:
            write_file_from_list('Abandoned_Airfield_addresses.txt', name_and_addresses_list)
        else:
            #print('Your data has been scrapped and kept into a list')
            return name_and_addresses_list


#   If You don't set a path for this function if you use it it will
#   just try to find the default name that the program made if there is one
#   otherwise just input the path
def remove_previous_file(path=None):
    try:
        os.remove(path)
    except:
        pass
    try:
        os.remove('Abandoned_Airfield_addresses.txt')
    except:
        pass


# This function also works as the "get_region_data" method in the way of making a file
# WARNING:
#       If you don't want a text file, you must set default_file_name variable as True
#       so it will return a text file with the default name
#       otherwise it will just return a list of the last
#       state data-set
def get_all_states(url, file_name=None, default_file_name=None):
    remove_previous_file(file_name)
    state_list = ['AL', 'IL', 'MT', 'PR', 'AK', 'IN', 'NE', 'RI', 'AZ', 'IA', 'NV', 'SC',
                  'AR', 'KS', 'NH', 'SD', 'CA', 'KY', 'NJ', 'TN', 'CO', 'LA', 'NM', 'TX',
                  'CT', 'ME', 'NY', 'UT', 'DE', 'MD', 'NC', 'VT', 'DC', 'MA', 'ND', 'VA',
                  'FL', 'MI', 'OH', 'WA', 'GA', 'MN', 'OK', 'WV', 'HI', 'MS', 'OR', 'WI',
                  'ID', 'MO', 'PA', 'WY']

    state_list_links = state_airfields_url(url, all_states=True)

    for index in range(0, len(state_list_links)):
        get_region_data(state_list_links[index], state_list[index], file_name, default_file_name)


def format_coordinates(my_file, index, formatted_file):
    my_file[index] = my_file[index].split('/')

    for new_index in range(0, len(my_file[index])):
        my_file[index][new_index] = my_file[index][new_index].lstrip(' ')
        my_file[index][new_index] = my_file[index][new_index].rstrip(' ')

    if 'North' in my_file[index][0]:
        my_file[index][0] = my_file[index][0].replace('North', '')
        my_file[index][0] = my_file[index][0].rstrip(' ')

        formatted_file += [str(my_file[index][0])]
    elif 'South' in my_file[index][0]:
        my_file[index][0] = my_file[index][0].replace('South', '')
        my_file[index][0] = my_file[index][0].rstrip(' ')

        formatted_file += [str(my_file[index][0])]
    if 'East' in my_file[index][1]:
        my_file[index][1] = my_file[index][1].replace('East', '')
        my_file[index][1] = my_file[index][1].rstrip(' ')

        formatted_file += [str(my_file[index][1])]
    elif 'West' in my_file[index][1]:
        my_file[index][1] = my_file[index][1].replace('West', '')
        my_file[index][1] = my_file[index][1].rstrip(' ')

        formatted_file += [str(my_file[index][1])]
        formatted_file += [str(1)]
        formatted_file += [str(0)]
        formatted_file += ['#AbandonedAirField']
        formatted_file += [None]
        formatted_file += ['']


def formatting_file(data):
    my_data = data
    my_data = filter(None, my_data)

    formatted_file = []
    index = 0
    while index < len(my_data):
        my_data[index] = my_data[index].split(',')

        formatted_file += [str(my_data[index][0])]
        index += 1
        if '(' in my_data[index]:
            if ')' in my_data[index]:
                my_data[index] = my_data[index].replace('(', '<')
                my_data[index] = my_data[index].replace(')', '>')

            #print(my_file[index])
        find_text = re.findall(r'(<.*>)', my_data[index])
        try:
            find_text = find_text[0]
        except:
            find_text = '-1'
        #print(find_text)
        if find_text is '-1':
            format_coordinates(my_data, index, formatted_file)
            index += 1
        elif find_text in my_data[index]:
            my_data[index] = my_data[index].replace(find_text, '')
            format_coordinates(my_data, index, formatted_file)
            index += 1

    return formatted_file


def main():
    url = 'http://www.airfields-freeman.com/NY/Airfields_NY.htm'
    state = 'NY'
    data = get_region_data(url, state, default_file_name=False)
    new_data = formatting_file(data)
    for index in range(0, len(new_data)):
        print(new_data[index])


main()