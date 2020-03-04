# -*- coding:utf-8
from main import error, api_response
from user.auth import check
from .main import get_full_kcb, get_mini_kcb, get_class_mate, intelligent_recommendation


@check
def get_schedule(request):
    if request.GET['type'] == 'full':
        result = get_full_kcb(request.user.person)
    elif request.GET['type'] == 'mini':
        result = get_mini_kcb(request.user.person)
    else:
        result = []
    return api_response({'data': result})


@check
def get_classmate(request):
    course_id, course_no = request.GET['course'].split('_')
    result = get_class_mate(course_id, course_no)
    return api_response({'data': result})


@check
def get_intelligent_recommendation(request):
    return api_response({'data': intelligent_recommendation(request.user.person)})
