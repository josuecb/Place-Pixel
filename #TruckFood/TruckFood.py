__author__ = 'Josue Carbonel'

import requests


# get_data_from Returns a list in this format:
#       name
#       Latitude
#       Longitude
# even though it returns a list of many trucks found in the page
def get_data_from(url):
    response = requests.get(url)
    response = response.content
    response = response.lstrip('[')
    response = response.rstrip(']')
    response = str(response).split(',')

    index_name = []         # Gets all indexes where the truck names are
    index_lat = []          # Gets the index where the lat of the truck are
    index_long = []         # Gets the index where the long of the truck are

    for i in range(0, len(response)):
        if '"name"' in response[i]:             # Finds the indexes
            index_name += [i]
        if '"latitude"' in response[i]:         # Finds the truck lat
            index_lat += [i]
        if '"longitude"' in response[i]:        # Finds the truck long
            index_long += [i]

    truck_and_address_list = []
    for i in range(0, len(index_name)):
        response[index_name[i]] = response[index_name[i]].replace('"name":', '').replace('"', '')
        #print(response[index_name[i]])
        truck_and_address_list += [str(response[index_name[i]])]
        response[index_lat[i]] = response[index_lat[i]].replace('"latitude":', '').replace('"', '')
        #print(response[index_lat[i]])
        truck_and_address_list += [str(response[index_lat[i]])]
        response[index_long[i]] = response[index_long[i]].replace('"longitude":', '').replace('"', '')
        #print(response[index_long[i]])
        truck_and_address_list += [str(response[index_long[i]])]
        #print('')

    return truck_and_address_list


def scrapping_sites(zip_code_list):
    for index in range(0, len(zip_code_list)):
        url = 'http://nyctruckfood.com/api/trucks/search?q=' + str(zip_code_list[index])
        data_list = get_data_from(url)
        if index is 0:
            food_truck_list = data_list
        else:
            data_index = 0
            temp_list = []
            while data_index < len(data_list):
                truck_index = 0
                copy = False

                while truck_index < len(food_truck_list):
                    # This part of the program will compare if there is some place repeated in the zip code
                    # False mean do not copy and True means copy it
                    # If its repeated it will break the loop and it will stop looking for that place and will go
                    # to the next value.
                    # it also checks not only if the truck name is repeated it will also check the place
                    # it doesnt matter if it has the same name but it does if it has the name and the location
                    if data_list[data_index] == food_truck_list[truck_index]:
                        if data_list[data_index + 1] == food_truck_list[truck_index + 1]:
                            if data_list[data_index + 2] == food_truck_list[truck_index + 2]:
                                copy = False
                                break
                    else:
                        # It wont break until the loops ends because it will compare all the values
                        # what about if the first value is not the same as the middle one but
                        # at the end there is one duplicated value?
                        # that's why we do not break the loop until it ends
                        copy = True
                        truck_index += 3

                if copy is True:
                    # This will store only the data that is not repeated in a temp list
                    temp_list += [data_list[data_index]]        # Name
                    temp_list += [data_list[data_index + 1]]    # Lat
                    temp_list += [data_list[data_index + 2]]    # Long

                data_index += 3
            #print (temp_list)
            print('Found: ' + str(len(temp_list)/3) + ' TuckFoods without repetition in zip code: '
                  + str(zip_code_list[index]))

            food_truck_list += temp_list

        if index is len(zip_code_list)-1:
            return food_truck_list


def print_in_format_the(truck_list):
    data_list = filter(None, truck_list)

    index = 0
    while index < len(data_list):
        print(data_list[index])     # Name
        index += 1
        print(data_list[index])     # Latitude
        index += 1
        print(data_list[index])     # Longitude
        index += 1
        print('1')
        print('#TruckFood')
        print(None)
        print('')


if __name__ == '__main__':
    zip_code_list = [10001, 10002, 10003, 10004, 10005, 10006, 10007, 10009, 10010, 10011,
                     10012, 10013, 10014, 10016, 10017, 10018, 10019, 10020, 10021, 10022,
                     10023, 10024, 10025, 10026, 10027, 10028, 10029, 10030, 10031, 10032,
                     10033, 10034, 10035, 10036, 10037, 10038, 10039, 10040, 10044, 10065,
                     10069, 10075, 10103, 10110, 10111, 10112, 10115, 10119, 10128, 10152,
                     10153, 10154, 10162, 10165, 10167, 10168, 10169, 10170, 10171, 10172,
                     10173, 10174, 10177, 10199, 10271, 10278, 10279, 10280, 10282, 10301,
                     10302, 10303, 10304, 10305, 10306, 10307, 10308, 10309, 10310, 10311,
                     10312, 10314, 10451, 10452, 10453, 10454, 10455, 10456, 10457, 10458,
                     10459, 10460, 10461, 10462, 10463, 10464, 10465, 10466, 10467, 10468,
                     10469, 10470, 10471, 10472, 10473, 10474, 10475, 11004, 11005, 11101,
                     11102, 11103, 11104, 11105, 11106, 11109, 11201, 11203, 11204, 11205,
                     11206, 11207, 11208, 11209, 11210, 11211, 11212, 11213, 11214, 11215,
                     11216, 11217, 11218, 11219, 11220, 11221, 11222, 11223, 11224, 11225,
                     11226, 11228, 11229, 11230, 11231, 11232, 11233, 11234, 11235, 11236,
                     11237, 11238, 11239, 11351, 11354, 11355, 11356, 11357, 11358, 11359,
                     11360, 11361, 11362, 11363, 11364, 11365, 11366, 11367, 11368, 11369,
                     11370, 11371, 11372, 11373, 11374, 11375, 11377, 11378, 11379, 11385,
                     11411, 11412, 11413, 11414, 11415, 11416, 11417, 11418, 11419, 11420,
                     11421, 11422, 11423, 11424, 11425, 11426, 11427, 11428, 11429, 11430,
                     11432, 11433, 11434, 11435, 11436, 11451, 11691, 11692, 11693, 11694,
                     11697]
    # You have to wait a while because it will scrape all the zip code list
    truck_list = scrapping_sites(zip_code_list)
    print_in_format_the(truck_list)