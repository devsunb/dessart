import requests
import config


def eleven(access_token, class_num, seat_num):
    headers = {
        'Authorization': 'JWT ' + access_token,
        'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36', 'cookie': 'JWT=' + access_token}
    payload = {'class_num': (None, str(config.CLASSES[class_num])),
               'seat_num': (None, str(seat_num))}
    response = requests.post(config.URL_DMS + config.URL_EXTENTION_11,
                             files=payload, headers=headers)
    if response.status_code == 201:
        return True
    else:
        return False


def twelve(access_token, class_num, seat_num):
    headers = {
        'Authorization': 'JWT ' + access_token,
        'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36', 'cookie': 'JWT=' + access_token}
    payload = {'class_num': (None, str(config.CLASSES[class_num])),
               'seat_num': (None, str(seat_num))}
    response = requests.post(config.URL_DMS + config.URL_EXTENTION_12,
                             files=payload, headers=headers)
    if response.status_code == 201:
        return True
    else:
        return False
