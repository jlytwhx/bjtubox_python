from course.models import Course
from .models import Schedule
from main import get_now_week
from django.forms.models import model_to_dict
from freeclass.models import Classroom
import time
import random
import datetime
import requests


def get_token():
    api = ''
    data = {
        'loginname': '',
        'password': ''
    }
    data = requests.post(api, data).json(encoding='utf-8')
    token = data['token']
    return token


def get_class_mate(course_id, course_no):
    result = []
    student_list = Schedule.objects.filter(course_no=course_no, course_id=course_id)
    userid_list = []
    for student in student_list:
        name = student.student.name
        userid = student.student.id
        if userid in userid_list:
            continue
        userid_list.append(userid)
        stu_class = student.student.stu_class
        result.append({'name': name, 'userid': userid, 'stu_class': stu_class})
    return result


def get_course_list(person):
    result = []
    course_list = []
    if person.group.id == 1 or person.group_id == 4:
        for schedule in Schedule.objects.filter(student=person):
            course_info = Course.objects.filter(course_id=schedule.course_id, course_no=schedule.course_no)
            course_list += [*course_info]

    elif person.group.id == 0:
        api = ''.format(
            person.id, get_token())
        tasks = requests.get(api).json(encoding='utf-8')['objects']
        for task in tasks:
            course_list += [*Course.objects.filter(course_no=task['kxh'], course_id=task['kch'])]

    now_week = get_now_week()
    for course in course_list:
        if str(now_week) in course.week.split(','):
            result.append(course)
    return result


def get_full_kcb(person):
    course_list = get_course_list(person)
    result = [
        {'day': 1, 'course': []},
        {'day': 2, 'course': []},
        {'day': 3, 'course': []},
        {'day': 4, 'course': []},
        {'day': 5, 'course': []},
        {'day': 6, 'course': []},
        {'day': 7, 'course': []},
    ]
    for course in course_list:
        result[course.day - 1]['course'].append(model_to_dict(course))
    for day in result:
        day['course'] = sorted(day['course'], key=lambda x: x['day_no'])
    return result


def intelligent_recommendation(person):
    if person.group_id not in [1, 4]:
        return ''
    jobs = ['', '', '', '', '', '', '']
    time_list = ['8:00-9:50', '10:10-12:00', '12:10-14:00', '14:10-16:00', '16:20-18:10', '19:00-20:50', '21:00-22:00']
    now_day = datetime.datetime.now().weekday()
    schedule = get_full_kcb(person)[now_day]['course']
    for course in schedule:
        day_no = course['day_no']
        jobs[day_no - 1] = {
            'name': course['name'],
            'building': course['building'],
            'where': course['classroom'],
            'when': time_list[int(course['day_no']) - 1],
            'type': 1  # 1为正常课程 2为智能推荐
        }
    now_time = int(datetime.datetime.now().strftime('%H'))
    if now_time < 10:
        a = 0
    elif now_time < 12:
        a = 1
    elif now_time < 14:
        a = 2
    elif now_time < 16:
        a = 3
    elif now_time < 19:
        a = 4
    elif now_time < 21:
        a = 5
    elif now_time < 22:
        a = 6
    else:
        return []
    for index, job in list(enumerate(jobs))[a:]:
        if not job:
            try:
                last_building = jobs[index + 1]['building']
                last_classroom = jobs[index + 1]['where']
            except:
                try:
                    last_building = jobs[index - 1]['building']
                    last_classroom = jobs[index - 1]['where']
                except:
                    last_building = None
                    last_classroom = None
            search_dict = {
                'class{}'.format(index + 1): '空闲'
            }
            if last_building:
                search_dict['building'] = last_building
                search_dict['name__startswith'] = last_classroom[0]
                result = Classroom.objects.filter(**search_dict)
                if not result:
                    search_dict.pop('name__startswith')
                    result = Classroom.objects.filter(**search_dict)
                if not result:
                    search_dict.pop('building')
                    search_dict['building__in'] = ['思源西楼', '思源东楼', '思源楼', '逸夫教学楼', '机械楼', '第九教学楼']
                    result = Classroom.objects.filter(**search_dict)
            else:
                search_dict['building__in'] = ['思源西楼', '思源东楼', '思源楼', '逸夫教学楼', '机械楼', '第九教学楼']
                result = Classroom.objects.filter(**search_dict)
            if result:
                random_int = random.randint(0, len(result) - 1)
                jobs[index] = {
                    'name': '空闲教室推荐',
                    'building': result[random_int].building,
                    'where': result[random_int].name,
                    'when': time_list[index],
                    'type': 2
                }
    result = [job for job in jobs[a:] if job][:2]
    return result


def get_mini_kcb(person):
    result = []
    course_list = get_course_list(person)
    weekday = int(datetime.datetime.now().weekday()) + 1
    now_time = int(datetime.datetime.now().strftime('%H'))
    if now_time < 8:
        a = 0
    elif now_time < 10:
        a = 1
    elif now_time < 12:
        a = 2
    elif now_time < 14:
        a = 3
    elif now_time < 16:
        a = 4
    elif now_time < 19:
        a = 5
    elif now_time < 21:
        a = 6
    elif now_time < 22:
        a = 7
    else:
        a = 8
    for course in course_list:
        if course.day == weekday:
            if course.day_no >= a:
                data = dict()
                data['name'] = course.name
                data['where'] = course.classroom
                data['when'] = course.day_no
                result.append(data)
    result = sorted(result, key=lambda x: int(x['when']))[:2]
    if not result:
        result.append({
            'name': '今日已无课',
            'where': '',
            'when': ''
        })
    return result
