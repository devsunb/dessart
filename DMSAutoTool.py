# Reserve Extend Study Seat Code
# $.ajax({
#         url: "http://dsm2015.cafe24.com/apply/extension",
#         type: "PUT",
#         data: {
#             "class": classId,
#             "seat": id
#         },
#         statusCode: {
#             200: function() {
#                 alert("신청 완료되었습니다.");
#                 getClassData(classId);
#             },
#             204: function() {
#                 alert("신청가능한 시간이 아닙니다.");
#                 getClassData(classId);
#             },
#             500: function() {
#                 alert("신청중에 오류가 발생하였습니다.");
#                 getClassData(classId);
#             }
#         },
#         error: function(request, status, error) {
#             alert("신청중에 오류가 발생하였습니다.");
#             getClassData(classId);
#         }
#     });
# Login Code
# $.ajax({
#         url: "/account/login/student",
#         type: "POST",
#         data: {
#             id: $(".login-input #name").val(),
#             password: $(".login-input #pass").val(),
#             remember: $(".login-check input:checked").val()
#         },
#         success: function(data, status) {
#             location.reload();
#         },
#         error: function(xhr) {
#             alert("로그인에 실패했습니다.");
#         },
#     });

import requests

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
        print('[SUC] ' + id + ' : 로그인 성공 [' + cookie + ']')
        return True
    else:
        print('[ERR] ' + id + ' : 로그인 실패! [' + cookie + ']')
        return False


def reserveSeat(className, seat):
    global cookie

    # Reserve Seat
    url = "http://dsm2015.cafe24.com/apply/extension"
    payload = {'class': classList[className], 'seat': seat}
    headers = {
        'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36', 'cookie': cookie}
    response = requests.put(url, data=payload, headers=headers)
    if response.status_code == 200:
        print('[SUC] ' + ' : ' + className + ' ' + seat + '번 자리 신청 성공!')
        return
    elif response.status_code == 204:
        print('[ERR] ' + cookie[(cookie.find("vertx-web.session=") + 18):(cookie.find("vertx-web.session=") + 50)] + ' : 연장 가능 시간 아님! ' +
              className + ' ' + seat + '번 자리 신청 실패!')
        return
    else:
        print('[ERR] ' + ' : 오류 발생! ' +
              className + ' ' + seat + '번 자리 신청 실패!')
        return


if __name__ == '__main__':
    if(login('infreljs', '20412') == False):
        exit()
    reserveSeat('다온실', '14')
