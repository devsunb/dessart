import requests
import time

classes = {
    '다온실': '3',
    '나온실': '2',
    '가온실': '1',
    '라온실': '4',
    '4층 독서실': '6',
    '3층 독서실': '5',
    '5층 독서실': '7'
}

classList = ['다온실', '나온실', '가온실', '라온실', '4층 독서실', '3층 독서실', '5층 독서실']
seatList = [
    ['13', '14', '17', '18'],
    ['1', '3', '7', '11', '15'],
    ['1', '5', '9', '13', '17'],
    ['1', '5', '3', '13', '17'],
    ['1', '9', '17', '25'],
    ['1', '9', '17', '25'],
    ['6', '7', '8']
]

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
        payload = {'class': classes[className], 'seat': seat}
        headers = {
            'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36', 'cookie': cookie}
        response = requests.put(url, data=payload, headers=headers)
        if response.status_code == 200:
            print('[SUC] ' + cookie[(cookie.find("vertx-web.session=") + 18):(cookie.find(
                "vertx-web.session=") + 50)] + ' : ' + className + ' ' + seat + '번 자리 신청 성공!')
            return 0
        elif response.status_code == 204:
            print('[ERR] ' + cookie[(cookie.find("vertx-web.session=") + 18):(cookie.find(
                "vertx-web.session=") + 50)] + ' : 연장 가능 시간 아님! ' + className + ' ' + seat + '번 자리 신청 실패!')
        elif response.status_code == 400:
            print('[ERR] ' + cookie[(cookie.find("vertx-web.session=") + 18):(
                cookie.find("vertx-web.session=") + 50)] + ' : [400] 오류 발생! ' +
                className + ' ' + seat + '번 자리 신청 실패! 로그인 재시도...')
            login('infreljs', '20412')
        elif response.status_code == 500:
            print('[ERR] ' + cookie[(cookie.find("vertx-web.session=") + 18):(
                cookie.find("vertx-web.session=") + 50)] + ' : [500] 오류 발생! ' +
                className + ' ' + seat + '번 자리는 이미 신청된 자리입니다!!!')
            return 1

        counter += 1
        if counter >= 15:
            print('[FIN] ' + cookie[(cookie.find("vertx-web.session=") + 18):(cookie.find(
                "vertx-web.session=") + 50)] + ' : 시도 ' + str(counter) + '회 초과로 종료합니다.')
            return -1
        else:
            print('[~~~] ' + cookie[(cookie.find("vertx-web.session=") + 18)                                    :(cookie.find("vertx-web.session=") + 50)] + ' : 5초 후 다시 시도...')
            time.sleep(5)


if __name__ == '__main__':
    counter = 0
    now = time.localtime()

    print('---------- START AUTO RESERVE SEAT ----------')
    print("------ %04d년 %02d월 %02d일 %02d시 %02d분 %02d초 ------" % (now.tm_year, now.tm_mon,
                                                                 now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec))
    getSession()
    while login('infreljs', '20412') == False:
        counter += 1
        if counter >= 15:
            print('[FIN] 시도 ' + str(counter) + '회 초과로 종료합니다.')
            exit()
        else:
            print('[ERR] 로그인 실패!!! 5초 후 다시 시도...')
            time.sleep(5)

    for i in range(len(classList)):
        for j in range(len(seatList[i])):
            print('[~~~] ' + classList[i] + ' ' +
                  seatList[i][j] + '번 자리 신청 시도')
            result = reserveSeat(classList[i], seatList[i][j])
            if result == 1:
                continue
            else:
                exit()
