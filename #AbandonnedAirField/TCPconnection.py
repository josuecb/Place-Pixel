__author__ = 'Anonymous'

import socket
import threading
import requests
from lxml.html import fromstring
import math

def TCP_client():
    target_host = 'www.google.com'
    target_port = 80

    # create a socket object
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connect the client
    client.connect((target_host, target_port))

    # send some data
    client.send('GET / HTTP/1.1\r\nHost: google.com\r\n\r\n')

    # receive some data
    response = client.recv(4096)

    print(response)


def UDP_client():
    target_host = '127.0.0.1'
    target_port = 80

    # create a socket object
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # send some data
    client.sendto('AAABBBCCC', (target_host, target_port))

    # receive some data
    data, addr = client.recvfrom(4096)

    print(data)


def TCP_server():
    bind_ip = '0.0.0.0'
    bind_port = 9999


    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server.bind((bind_ip, bind_port))

    server.listen(5)

    print('[*] Listening n %s:%d' % (bind_ip, bind_port))

    # this is our client-handling thread

    def handle_client(client_socket):
        # print out what the client sends
        request = client_socket.recv(1024)

        print('[*] Received: %s' % request)

        # send back a packet
        client_socket.send('ACK!')

        client_socket.close()

    while True:
        client, addr = server.accept()
        print('[*] Accepted connection from %s:%d' % (addr[0], addr[1]))

        # spin up our client thread to handle incoming data
        client_handler = threading.Thread(target=handle_client, args=(client,))
        client_handler.start()


def forms():
    url = 'https://m.facebook.com/'
    response = requests.get(url)

    html = fromstring(response.content)
    print(html)

    payload = dict(html.forms[0].fields)
    print(payload)


def get_y(lat, height, width):
    PI = 3.14159265359
    latRad = lat * PI / 180

    mercN = math.log(math.tan((PI / 4) + (latRad / 2)))
    y = (height / 2) - (width * mercN / (2 * PI))

    return y



if __name__ == '__main__':
    y = get_y(40.7746, 116319.4, 448784.7)
    print(y)