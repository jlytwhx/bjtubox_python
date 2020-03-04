# -*- coding:utf-8 -*-
from network import get_network_base_info, get_online_list, offline_device
from user.auth import check
from main import api_response


@check
def get_info(request):
    user = request.user
    userid = user.person.id
    result = {
        'base_info': get_network_base_info(userid),
        'online_devices': get_online_list(userid)
    }
    return api_response(result)


@check
def offline(request):
    session_id = request.GET['session_id']
    user_id = request.user.person_id
    if offline_device(user_id, session_id):
        return api_response({
            'msg': '强制下线成功！'
        })
    else:
        return api_response({
            'code': 3501,
            'msg': '强制下线时发生未知错误'
        })
