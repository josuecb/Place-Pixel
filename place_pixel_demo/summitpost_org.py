from commonutil import do_request
from lxml import html, etree
import string
import re

def scrape_images(image):
    page = do_request("http://www.summitpost.org" + image)
    tree = html.fromstring(page)
    img_url = tree.xpath('//*[@id="main_photo"]/tr/td/table/tr/td/div/a/img/@src')
    if img_url and len(img_url) > 0:
        return img_url[0]
    else:
        return None

def scrape_link(link):
    page = do_request("http://www.summitpost.org" + link)
    tree = html.fromstring(page)
    page_title = tree.xpath('//*[@id="main_data_box"]/table/tr/td/header/h1')[0].text
    lat_lon = tree.xpath('//*[@id="main_data_box"]/table/tr/td/p[3]/a')[0].text

    latraw, lonraw = lat_lon.split("/")
    lat = re.search("(\d+(\.\d+)?)", latraw).group(1)
    lon = re.search("(\d+(\.\d+)?)", lonraw).group(1)

    if 'S' in latraw:
        lat = -float(lat)
    if 'W' in lonraw:
        lon = -float(lon)

    hits_raw = etree.tostring(tree.xpath('//*[@id="main_data_box"]/table/tr/td[2]/p[4]')[0])
    hits = int(re.search('(\d+)', hits_raw).group(1))

    activities = 'None'
    try:
        activities_raw = etree.tostring(tree.xpath('//*[@id="main_data_box"]/table/tr/td[1]/p[5]')[0])
        if 'Activities' in activities_raw:
            am_regex = re.search('\s(([a-zA-Z\s?]+)(\,\s)?)+', activities_raw)
            if am_regex:
                am = am_regex.group(0).strip().split(', ')
                activities = ' '.join(['#' + amm for amm in am])
    except:
        pass

    image_urls = 'None'
    try:
        images = tree.xpath('//*[@id="my_images"]/tr/td/a/@href')
        #image_urls = ' '.join([scrape_images(img) for img in images])
    except:
        pass

    print(page_title)
    print(lat)
    print(lon)
    print(int(round(hits / 1000)))
    print(0)
    print(activities.lower())
    print(image_urls)

def scrape_letter(url, visited):
    visited.add(url)
    page = do_request(url)
    tree = html.fromstring(page)
    object_links = tree.xpath('//*[@id="results"]/table/tr/td/a/@href')

    links_set = set()
    links = []
    for link in object_links:
        m = re.search(r'\/(\d+$)', link)
        if m and m.group(1) not in links_set:
            links_set.add(m.group(1))
            links.append(link)
            try:
                scrape_link(link)
            except Exception as e:
                pass
            print('')

    next_page = tree.xpath('//*[@id="content"]/div/div/table/tr/td/a[starts-with(text(), "NEXT")]/@href')
    if len(next_page) > 0 and next_page[0] not in visited:
        scrape_letter("http://www.summitpost.org" + next_page[0], visited)

if __name__ == '__main__':
    visited = set()
    for letter in string.ascii_uppercase:
        url = "http://www.summitpost.org/object_list.php?object_type=1&letter=" + letter
        scrape_letter(url, visited)
