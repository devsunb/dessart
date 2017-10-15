import requests
import time

classList = {
    '가온실': '1',
    '나온실': '2',
    '다온실': '3',
    '라온실': '4',
    '3층 독서실': '5',
    '4층 독서실': '6',
    '5층 독서실': '7'
}

cookie = ''


def getSession():
    global cookie

    # Get Session
    url = "http://dsm2015.cafe24.com/"
    headers = {
        'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36', 'cookie': cookie}
    response = requests.get(url, headers=headers)
    cookie = response.headers['Set-Cookie']


def login(id, pw):
    global cookie

    # Login
    url = "http://dsm2015.cafe24.com/account/login/student"
    payload = {'id': id, 'password': pw, 'remember': 'undefined'}
    headers = {
        'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36', 'cookie': cookie}
    response = requests.post(url, data=payload, headers=headers)
    cookie = response.headers['Set-Cookie']
    if response.status_code == 201:
        print('[SUC] ' + id + ' : 로그인 성공 [' + cookie[(cookie.find("vertx-web.session=") + 18):(cookie.find(
            "vertx-web.session=") + 50)] + ']')
        return True
    else:
        print('[ERR] ' + id + ' : 로그인 실패! [' + cookie[(cookie.find("vertx-web.session=") + 18):(cookie.find(
            "vertx-web.session=") + 50)] + ']')
        return False


def reserveSeat(className, seat):
    global cookie
    counter = 0

    # Reserve Seat
    while True:
        url = "http://dsm2015.cafe24.com/apply/extension"
        payload = {'class': classList[className], 'seat': seat}
        headers = {
            'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36', 'cookie': cookie}
        response = requests.put(url, data=payload, headers=headers)
        if response.status_code == 200:
            print('[SUC] ' + cookie[(cookie.find("vertx-web.session=") + 18):(cookie.find(
                "vertx-web.session=") + 50)] + ' : ' + className + ' ' + seat + '번 자리 신청 성공!')
            return
        elif response.status_code == 204:
            print('[ERR] ' + cookie[(cookie.find("vertx-web.session=") + 18):(cookie.find(
                "vertx-web.session=") + 50)] + ' : 연장 가능 시간 아님! ' + className + ' ' + seat + '번 자리 신청 실패!')
        elif response.status_code == 400:
            print('[ERR] ' + cookie[(cookie.find("vertx-web.session=") + 18):(
                cookie.find("vertx-web.session=") + 50)] + ' : [400] 오류 발생! ' +
                className + ' ' + seat + '번 자리 신청 실패! 로그인 재시도...')
            login('infreljs', '20412')

        counter += 1
        if counter >= 30:
            print('[FIN] ' + cookie[(cookie.find("vertx-web.session=") + 18):(
                cookie.find("vertx-web.session=") + 50)] + ' : 시도 ' + str(counter) + '회 초과로 종료합니다.')
            return
        else:
            print('[~~~] ' + cookie[(cookie.find("vertx-web.session=") + 18):(cookie.find("vertx-web.session=") + 50)] + ' : 10초 후 다시 시도...')
            time.sleep(10)


if __name__ == '__main__':
    getSession()
    if(login('infreljs', '20412') == False):
        print('[ERR] 로그인 실패! 로그인 재시도...')
        exit()
    reserveSeat('다온실', '14')
