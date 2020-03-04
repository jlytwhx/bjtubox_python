import time
import uuid
import json
import hashlib
import requests


# from .models import Person


class MobileBjtu:
    def __init__(self):
        self.session = requests.session()
        self.session.headers.update(
            {
                "Content-Type": 'application/json;charset=UTF-8',
                "Accept-Encoding": 'gzip, deflate',
                'Accept-Language': 'cn',
                "User-Agent": 'Mozilla/5.0 (Linux; Android 7.0; SM-G9300 Build/NRD90M) AppleWebKit/537.36 (KHTML, '
                              'like Gecko) Chrome/48.0.2564.116 Crosswalk/18.48.477.13 Mobile Safari/537.36',
                "Accept": 'application/json, text/plain, */*',
                "token": '',
                "Origin": "file://"
            }
        )
        token = self.login()
        self.session.headers['token'] = token

    @staticmethod
    def signature(data):
        keys = list()
        for key in data:
            keys.append(key)
        keys.sort()
        a = ''
        for key in keys:
            a += key + '=' + data[key]
            a += '&'
        a = a[:-1]
        md5 = hashlib.md5(a.encode())
        signature = md5.hexdigest()
        return signature

    def login(self, userid, password):
        unix_stamp = str(int(time.time()))
        uid = str(uuid.uuid4())
        post_data = {
            "appKey": "GiITvn",
            "time": unix_stamp,
            "secure": "0",
            'param': json.dumps({
                'userName': userid,
                'password': password,
                'uuId': uid,
                'schoolId': '158'
            }, ensure_ascii=False)
        }
        post_data['sign'] = self.signature(post_data)
        url = ''
        page = self.session.post(url, json.dumps(post_data, ensure_ascii=False)).content.decode()
        token = json.loads(page)['token'][0] + '_' + json.loads(page)['token'][1]
        return token

    def get_person_data(self, student):
        unix_stamp = str(int(time.time()))
        url = ''
        post_data = {
            "appKey": "GiITvn",
            "time": unix_stamp,
            "secure": "0",
            "param": json.dumps({
                'xgh': student.id,
                'offset': 1,
                'role': 272,
                'menuId': 1
            }, ensure_ascii=False)
        }
        post_data['sign'] = self.signature(post_data)
        page = self.session.post(url, json.dumps(post_data, ensure_ascii=False)).content.decode()
        print(page)
        info = json.loads(page)['userList'][0]
        stu_class = info['classId']
        school = info['collegeName']
        avatar = info['headImage']
        name = info['realName']
        unknown_id = info['userId']
        profession = info['zymc']
        grade = info['sznj']
        sex = '女' if str(info['sex']) == '2' else '男'
        student.save()
        print(student_id, stu_class, province, nation, idcard, phone)

    def run(self, grade):
        for student in Person.objects.filter(id__istartswith=grade):
            if student.id_card or len(student.id) < 8:
                continue
            self.get_person_data(student)


if __name__ == '__main__':
    m = MobileBjtu()
    m.get_person_data('16211268')
