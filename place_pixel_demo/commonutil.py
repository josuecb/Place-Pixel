import requests
import redis

r = redis.StrictRedis(host='localhost', port=6379, db=0)

def do_request(url):
    result = r.get(url)
    if result:
        return result

    result = requests.get(url)
    r.set(url, result.text)
    return result.text


