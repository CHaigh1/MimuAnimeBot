import random
import string
import requests

def getImage():
    valid = False
    code = ''

    while not valid:
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        response = requests.get('http://i.imgur.com/' + code + '.jpg')
        if response.status_code == 200:
            if response.headers['Content-Length'] != '503':
                valid = True

    return 'http://i.imgur.com/' + code + '.jpg'