__author__ = 'Anonymous'


def print_in_format(data_list):
    """ This will print the file in the following format
          Name
          Address
          Long
          1
          #tag
          None
          space"""
    data_list = filter(None, data_list)

    index = 0
    while index < len(data_list):
        print(data_list[index])
        index += 1
        print(data_list[index])
        index += 1
        print('long')
        print('1')
        print('#ApplePay')
        print(None)
        print('')


