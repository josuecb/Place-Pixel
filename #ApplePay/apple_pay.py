"""This script will display all the Stores that Accept ApplePay Payment
    in the format wanted"""
__author__ = 'Josue Carbonel'

from aeropostal_stores import print_aeropostale_stores
from apple_stores import print_apple_store_content
from bjs_stores import print_bjs_stores
from bloomingdales_stores import print_bloomingdales_stores
from champssport_stores import print_champssports_stores
from foot_action_stores import print_foot_action_stores
from foot_locker_stores import print_footlocker_stores
from macys import print_macys_stores
from toy_r_us_stores import print_toy_r_us_stores
from mc_donals import printing_mcdonals_stores


def printing_all_stores():
    """ Every method used in this method will print each store
        in the write format wanted
        for more details just read the different files it has
        They are not big and there are like 5 or 4 different files that uses 1 API
        All the files now has comments and the right variable names"""
    print_aeropostale_stores()
    print_apple_store_content()
    print_bjs_stores()
    print_bloomingdales_stores()
    print_champssports_stores()
    print_foot_action_stores()
    print_footlocker_stores()
    print_macys_stores()
    print_toy_r_us_stores()
    printing_mcdonals_stores()


if __name__ == '__main__':
    printing_all_stores()

