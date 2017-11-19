import requests
import time
import sys

classes = {
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


def reserveSeat(id, class_, seat, t):
    global cookie
    counter = 0

    # Reserve Seat
    while True:
        url = "http://dsm2015.cafe24.com/apply/extension" + t
        payload = {'class': classes[class_], 'seat': seat}
        headers = {
            'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36', 'cookie': cookie}
        response = requests.put(url, data=payload, headers=headers)
        if response.status_code == 200:
            print('[SUC] ' + t + '시 (' + id + ') : ' + class_ +
                  ' ' + seat + '번 자리 신청 성공!')
            return 0
        elif response.status_code == 204:
            print('[ERR] ' + t + '시 (' + id + ') : 연장 가능 시간 아님! ' +
                  class_ + ' ' + seat + '번 자리 신청 실패!')
        elif response.status_code == 400:
            print('[ERR] ' + t + '시 (' + id + ') : [400] 오류 발생! ' +
                  class_ + ' ' + seat + '번 자리 신청 실패! 로그인 재시도...')
            login('infreljs', '20412')
        elif response.status_code == 500:
            print('[ERR] ' + t + '시 (' + id + ') : [500] 오류 발생! ' +
                  class_ + ' ' + seat + '번 자리는 이미 신청된 자리입니다!!!')
            return 1

        counter += 1
        if counter >= 15:
            print('[FIN] ' + id + ' : 시도 ' + str(counter) + '회 초과로 종료합니다.')
            return -1
        else:
            print('[~~~] ' + id + ' : 5초 후 다시 시도...')
            time.sleep(5)


def autoReserveSeat(id, pw, class_, seat, t):
    counter = 0
    now = time.localtime()

    print('---------- START AUTO RESERVE SEAT ----------')
    print("------ %04d년 %02d월 %02d일 %02d시 %02d분 %02d초 ------" % (now.tm_year, now.tm_mon,
                                                                 now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec))
    getSession()
    while login(id, pw) == False:
        counter += 1
        if counter >= 15:
            print('[FIN] 시도 ' + str(counter) + '회 초과로 종료합니다.')
            exit()
        else:
            print('[ERR] 로그인 실패!!! 5초 후 다시 시도...')
            time.sleep(5)

    print('[~~~] ' + class_ + ' ' + seat + '번 자리 신청 시도')
    result = reserveSeat(id, class_, seat, t)
    print('---------- END AUTO RESERVE SEAT ----------\n')
    exit()


if __name__ == '__main__':
    try:
        sel = sys.argv[sys.argv.index('-m') + 1]
        if(sel == 'seat'):
            id = sys.argv[sys.argv.index('-u') + 1]
            pw = sys.argv[sys.argv.index('-p') + 1]
            class_ = sys.argv[sys.argv.index('-c') + 1]
            seat = sys.argv[sys.argv.index('-s') + 1]
            t = sys.argv[sys.argv.index('-t') + 1]

            autoReserveSeat(id, pw, class_, seat, t)
        else:
            print('Usage : ' + sys.argv[0] +
                  ' -m (seat|weekend) -u (id) -p (password) -c (class) -s (seat) -t (time)')
            exit()

    except (ValueError, IndexError) as e:
        print('Usage : ' + sys.argv[0] +
              ' -m (seat|weekend) -u (id) -p (password) -c (class) -s (seat) -t (time)')
        exit()
