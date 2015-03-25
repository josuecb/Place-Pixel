__author__ = 'Josue Carbonel'

from store_locator import getting_addresses


def print_foot_action_stores():
    """ This Will use the  the storeLocator python Script API to scrape the page
        Read StoreLocator API for more details"""
    url = 'http://www.store-locator.info/footaction-usa/state/new-york'
    getting_addresses(url)
