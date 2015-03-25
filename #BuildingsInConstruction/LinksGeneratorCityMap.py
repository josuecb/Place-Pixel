__author__ = 'Anonymous'

import mechanize
import requests
from termcolor import colored
from unidecode import unidecode


lk1 = 'http://gis.nyc.gov/doitt/webmap/Identify?_v=%2215.0.0.3-73%22&identifyRequests=%5B%7B%22name%22%3A%22basemap%22%2C%22declaredClass%22%3A%22IdR%22%7D%2C%7B%22name%22%3A%22PB_STRPRO%22%2C%22declaredClass%22%3A%22IdR%22%7D%5D&geom=%7B%22declaredClass%22%3A%22PiG%22%2C%22point%22%3A%7B%22declaredClass%22%3A%22IP%22%2C%22x%22%3A'
lk2 = '%2C%22y%22%3A'
lk3 = '%7D%7D&mapData=%7B%22applicationName%22%3A%22DEFAULT%22%2C%22cacheName%22%3A%22GISBasic%22%2C%22declaredClass%22%3A%22MD%22%2C%22markupType%22%3A%22svg%22%2C%22newViewportDescription%22%3A%7B%22declaredClass%22%3A%22ID%22%2C%22height%22%3A625%2C%22mapEnvelope%22%3A%7B%22declaredClass%22%3A%22ME%22%2C%22height%22%3A1025808%2C%22maxX%22%3A1025808%2C%22maxY%22%3A1025808%2C%22minX%22%3A1025808%2C%22minY%22%3A191582%2C%22width%22%3A1025808%7D%2C%22offset%22%3A%7B%22declaredClass%22%3A%22IP%22%2C%22x%22%3A'
x2 = '0'
lk4 = '%2C%22y%22%3A'
y2 = '0'
lk5 = '%7D%2C%22width%22%3A1034%7D%2C%22previousViewportDescription%22%3A%7B%22declaredClass%22%3A%22ID%22%2C%22height%22%3A625%2C%22mapEnvelope%22%3A%7B%22declaredClass%22%3A%22ME%22%2C%22height%22%3A1025808%2C%22maxX%22%3A1025808.8%2C%22maxY%22%3A193752.2%2C%22minX%22%3A1022218.5%2C%22minY%22%3A191582%2C%22width%22%3A1025808%7D%2C%22offset%22%3A%7B%22declaredClass%22%3A%22IP%22%2C%22x%22%3A'
lk6 = '%7D%2C%22width%22%3A1034%7D%2C%22searches%22%3A%5B%5D%2C%22tileCacheDescription%22%3A%7B%22declaredClass%22%3A%22MID%22%2C%22height%22%3A1025808%2C%22mapEnvelope%22%3A%7B%22declaredClass%22%3A%22ME%22%2C%22height%22%3A1025808%2C%22maxX%22%3A1025808%2C%22maxY%22%3A1025808%2C%22minX%22%3A1025808%2C%22minY%22%3A1025808%2C%22width%22%3A1025808%7D%2C%22width%22%3A2560%7D%2C%22visibleCompoundFeatureTypeNames%22%3A%5B%22DDC_PROJECTS%22%5D%2C%22zoomLevel%22%3A8%2C%22cumulativeMapDrag%22%3A%7B%22declaredClass%22%3A%22IP%22%2C%22x%22%3A0%2C%22y%22%3A0%7D%2C%22featuresByNames%22%3A%5B%5D%7D&applicationName=%22DEFAULT%22&cumulativeMapDrag=%7B%22declaredClass%22%3A%22IP%22%2C%22x%22%3A0%2C%22y%22%3A0%7D&featureTypeNames=%5B%22basemap%22%5D'
x1 = '947'
y1 = '03'


def link_print():
    #url = lk1 + x1 + lk2 + y1 + lk3 + x2 + lk4 + y2 + lk5 + x2 + lk4 + y2 + lk6
    x = 0
    while x < 1000:
        y = 0
        while y < 1000:
            url = lk1 + str(x) + lk2 + str(y) + lk3 + x2 + \
                  lk4 + y2 + lk5 + x2 + lk4 + y2 + lk6

            print(url)
            print(x)
            print(y)
            response = requests.get(url,
                                    headers={"User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64)"
                                                           " AppleWebKit/537.36 (KHTML, like Gecko)"
                                                           " Chrome/40.0.2214.115 Safari/537.36"})
            response = str(response.content)
            if '{}&&"Your HTTP request has been blocked by our servers because it ' \
               'appears that you are utilizing this site in an unauthorized manner.' \
                    in response or '{}&&null' in response:
                print(response)
            elif 'PLUTO' in response:
                print colored('PLUTO', 'green')
            else:
                print colored(response, 'red')
                try:
                    open_file = open('valid_coordinates.txt').read()
                    open_file = open_file.split('\n')
                    open_file = filter(None, open_file)
                    if response in open_file:
                        print colored('already in', 'cyan')
                        pass
                    else:
                        my_file = open('valid_coordinates.txt', 'a')
                        my_file.write(response + '\n')
                        my_file.close()
                except Exception as error:
                    print colored(error, 'yellow')
                    my_file = open('valid_coordinates.txt', 'a')
                    my_file.write(response + '\n')
                    my_file.close()

            y += 1
        x += 1


if __name__ == '__main__':
    link_print()