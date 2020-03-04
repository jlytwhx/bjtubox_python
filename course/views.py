# -*- coding:utf-8 -*-
from main import api_response
from django.forms.models import model_to_dict
from course.models import Course
from user.auth import check
from person.models import Person


@check
def get_detail_info(request):
    course = Course.objects.get(id=request.GET['id'])
    result = model_to_dict(course)
    return api_response(result)


@check
def search(request):
    original_dict = dict(request.GET)
    original_dict.pop('sn')
    original_dict.pop('ts')
    page_size = min(int(original_dict.pop('page_size')[0]), 100)
    page = int(original_dict.pop('page')[0])
    search_dict = dict()
    for k in original_dict:
        if k == 'name':
            search_dict[k + '__contains'] = original_dict[k][0]
        elif k == 'teacher':
            search_dict['teacher__name__contains'] = original_dict[k][0]
        elif k == 'week':
            week = original_dict[k][0]
            search_dict[k + '__regex'] = r'(,%s,|^%s,|,%s$)' % (week, week, week)
        elif original_dict[k]:
            search_dict[k] = original_dict[k][0]
    course_list = [model_to_dict(x) for x in
                   Course.objects.filter(**search_dict)[(page - 1) * page_size: page * page_size]]
    for course in course_list:
        if course['teacher']:
            try:
                course['teacher'] = Person.objects.get(id=course['teacher']).name
            except:
                course['teacher'] = 'None'
    return api_response({'data': course_list})


@check
def get_base_info(request):
    get_classroom = lambda building: Course.objects.filter(building=building).values("classroom").distinct().order_by(
        "classroom")
    building_list = Course.objects.values("building").distinct()
    school_list = Course.objects.values("school").distinct()
    return api_response(
        {
            'building_list': {x['building']: [y['classroom'] for y in get_classroom(x['building'])] for x in
                              building_list},
            'school_list': [x['school'] for x in school_list]
        }
    )
