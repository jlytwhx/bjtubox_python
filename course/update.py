import requests
import json
from .models import Course


def get_token():
    api = ''
    data = {
        'loginname': '',
        'password': ''
    }
    data = requests.post(api, data).json(encoding='utf-8')
    token = data['token']
    return token


def get_name_and_point(token, course_id):
    url = ''
    params = {
        'token': token,
        'kch': course_id
    }
    content = requests.get(url, params=params).content.decode()
    data = json.loads(content, encoding='utf-8')['objects']
    if data:
        data = data[0]
    else:
        return None
    name = data['kcm']
    point = float(data['xf'])
    if data['xs']:
        hour = int(float(data['xs']))
    else:
        hour = 0
    return name, point, hour


def get_teacher_info(token, course_id, course_no):
    url = ''
    params = {
        'token': token,
        'kch': course_id,
        'kxh': course_no,
        'zxjxjhh': '2019-2020-1-2'
    }
    content = requests.get(url, params=params).content.decode()
    data = json.loads(content, encoding='utf-8')['objects'][0]
    teacher_id = data['jsh']
    return teacher_id


def get_place_and_time(token, api=None):
    if not api:
        api = ''
    params = {
        'token': token,
        'limit': 1000
    }
    response = requests.get(api, params=params)
    content = response.content.decode()
    data = json.loads(content, encoding='utf-8')
    course_list = data['objects']
    for course in course_list:
        course_id = course['kch']
        course_no = course['kxh']
        building = course['jxlm']
        classroom = course['jasm']
        week = ','.join([str(x + 1) for x, flag in enumerate(course['skzc']) if flag == '1'])
        weekday = course['skxq']
        day_no = course['skjc']
        name, point, hour = get_name_and_point(token, course_id)
        teacher_id = get_teacher_info(token, course_id, course_no)
        Course.objects.create(name=name, course_id=course_id, course_no=course_no, building=building,
                              classroom=classroom, week=week, day=weekday, day_no=day_no, point=point, hour=hour,
                              teacher_id=teacher_id, school='未知').save()
        print(course_id, course_no, building, classroom, week, weekday, day_no, name, point, hour, teacher_id)

    if data['meta']['next']:
        get_place_and_time(token, '' + data['meta']['next'])


def run():
    token = get_token()
    get_place_and_time(token)
