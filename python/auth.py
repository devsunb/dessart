import time
import requests
import config


def auth(user):
    headers = {
        'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
    payload = {'id': (None, user['id']), 'pw': (None, user['pw'])}
    response = requests.post(config.URL_DMS + config.URL_AUTH,
                             files=payload, headers=headers)
    if response.status_code == 200:
        access_token = response.json()['access_token']
        print('[+] 로그인 성공 : ' + user['id'])
        return access_token
