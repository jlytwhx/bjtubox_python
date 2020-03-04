# -*- coding:utf-8 -*-
from user.auth import check
from .models import Classroom
from .main import get_free_classroom_by_building_and_no
from django.forms.models import model_to_dict
from main import api_response


# Create your views here.
@check
def get_free_classroom(request):
    building_dict = {
        '学活': '学生活动服务中心',
        '八教': '第八教学楼',
        '东一': '东区一教',
        '东二': '东区二教',
        '思东': '思源东楼',
        '思西': '思源西楼',
        '思源': '思源楼',
        '逸夫': '逸夫教学楼',
        '机械': '机械楼',
        '九教': '第九教学楼',
        '五教': '第五教学楼',
        '建艺': '第十七号教学楼'
    }
    building = building_dict[request.GET['building']]
    no = request.GET['no']
    result = get_free_classroom_by_building_and_no(building, no)
    return api_response({'data': result})


@check
def get_classroom_status(request):
    classroom = request.GET['classroom']
    classroom = Classroom.objects.get(name=classroom)
    return api_response({'data': model_to_dict(classroom)})
