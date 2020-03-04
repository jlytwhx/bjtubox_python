import json
import requests
from .models import Person, Group


def get_token():
    api = ''
    data = {
        'loginname': '',
        'password': ''
    }
    data = requests.post(api, data).json(encoding='utf-8')
    token = data['token']
    return token


def get_student_data(token, api=None):
    if not api:
        api = ''.format(token)
    content = requests.get(api).content.decode()
    data = json.loads(content)
    student_list = data['objects']
    for student in student_list:
        student_id = student['xh']
        name = student['xm']
        school = student['xym']
        profession = student['zym']
        nation = student['mz']
        class_name = student['bm']
        grade = student['njdm']
        stu_type = student['pyccmc']
        if stu_type != '本科生':
            continue
        person = Person.objects.filter(id=student_id)
        if person:
            person = person[0]
            person.school = school
            person.profession = profession
            person.stu_class = class_name
            person.grade = grade
            person.save()
        else:
            person = Person.objects.create(
                id=student_id,
                school=school,
                profession=profession,
                stu_class=class_name,
                grade=grade,
                name=name,
                nation=nation,
                group=Group.objects.get(name='本科生')
            )
            person.save()
            print(name, student_id, class_name)
    if data['meta']['next']:
        get_student_data(token, '' + data['meta']['next'])


def run():
    token = get_token()
    get_student_data(token)
