__author__ = 'Josue Carbonel'

from my_store411 import getting_store_list
from formating_name_address import print_in_format


def print_bloomingdales_stores():
    """ This Will use the  the myStore411 python Script API to scrape the page"""
    url = 'http://mystore411.com/store/listing/96/Bloomingdale%27s-store-locations'
    data = getting_store_list(url)          # Store Lists in Name and Address
    print_in_format(data)                   # Prints it in the right format
