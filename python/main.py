import sys
import time
import auth
import extension


def main():
    try:
        user_id = sys.argv[sys.argv.index('-u') + 1]
        user_pw = sys.argv[sys.argv.index('-p') + 1]
        class_num = sys.argv[sys.argv.index('-c') + 1]
        seat_num = sys.argv[sys.argv.index('-s') + 1]
        t = sys.argv[sys.argv.index('-t') + 1]

    except (ValueError, IndexError):
        print('Usage : ' + sys.argv[0] +
              ' -u (id) -p (password) -c (class) -s (seat) -t (time)')
        exit()

    now = time.localtime()
    print("------ %04d년 %02d월 %02d일 %02d시 %02d분 %02d초 ------" % (now.tm_year, now.tm_mon,
                                                                 now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec))

    access_token = auth.auth({'id': user_id, 'pw': user_pw})
    counter = 1
    while access_token == False:
        if counter >= 15:
            print('[x] 시도 ' + str(counter) + '회 초과로 종료합니다.')
            exit()
        else:
            print('[!] 로그인 실패!!! 5초 후 다시 시도...')
            time.sleep(5)
        access_token = auth.auth({'id': user_id, 'pw': user_pw})
        counter += 1

    print('[+] 로그인 성공 : ' + user_id)
    print('[ ] (' + user_id + ') ' + t + '시 ' +
          class_num + ' ' + seat_num + '번 자리 신청 시도')

    if t == '11':
        counter = 1
        while extension.eleven(access_token, class_num, seat_num) == False:
            if counter >= 15:
                print('[x] 시도 ' + str(counter) + '회 초과로 종료합니다.')
                exit()
            else:
                print('[!] 연장 신청 실패!!! 5초 후 다시 시도...')
                time.sleep(5)
            counter += 1
    elif t == '12':
        counter = 1
        while extension.twelve(access_token, class_num, seat_num) == False:
            if counter >= 15:
                print('[x] 시도 ' + str(counter) + '회 초과로 종료합니다.')
                exit()
            else:
                print('[!] 연장 신청 실패!!! 5초 후 다시 시도...')
                time.sleep(5)
            counter += 1

    print('---------- END ----------\n')
    exit()


if __name__ == '__main__':
    main()
