# -*- coding:utf-8 -*-
from main import api_response
from .main import get_point
from user.auth import check


@check
def get_stu_point(request):
    user = request.user
    person = user.person
    data = get_point(person.id)
    return api_response({'data': data})
