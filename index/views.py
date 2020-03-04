# -*- coding:utf-8 -*-
import time

from ecard import get_ecard_balance
from main import api_response, get_now_week
from morning.main import is_morning_sign
from network import get_network_base_info, get_online_list
from schedule.main import intelligent_recommendation
from user.auth import check
from .main import get_menu_list, get_welcome


@check
def get_base_info(request):
    user = request.user
    person_id = user.person.id
    network_info = get_network_base_info(person_id)
    base_info = {
        'balance': str(get_ecard_balance(person_id)),
        'online_device_num': len(get_online_list(person_id)),
        'network_percent': str(100 - ((network_info['use_flow'] * 100) // (
                network_info['package_flow'] + network_info['carry_over_flow']))) + '%'
    }
    return api_response(base_info)


@check
def get_index_info(request):
    user = request.user
    person = request.user.person
    menu = get_menu_list(person)
    person_info = {
        'name': person.name,
        'sex': person.sex,
        'school': person.school,
        'class': person.stu_class,
        'type': person.group.name,
        'userid': person.id
    }
    wx_info = {
        'nickname': user.nickname,
        'avatar': user.avatar,
        'city': user.city
    }
    # mini_schedule = get_mini_kcb(person)
    """
    network_info = get_network_base_info(person.id)
    base_info = {
        'balance': str(get_ecard_balance(person.id)),
        'online_device_num': len(get_online_list(person.id)),
        'network_percent': str(100 - ((network_info['use_flow'] * 100) // (
                network_info['package_flow'] + network_info['carry_over_flow']))) + '%'
    }
    """
    chinese_num = ['', '一', '二', '三', '四', '五', '六', '七', '八', '九', '十', '十一', '十二', '十三', '十四', '十五', '十六', '十七', '十八',
                   '十九', '二十', '二十一', '二十二', '二十三', '二十四']
    day = int(time.strftime("%w", time.localtime()))
    day = day if day else 7
    if int(get_now_week()) < 18:
        week = '第' + chinese_num[int(get_now_week())] + '教学周 ' \
               + '星期' + ('日' if chinese_num[day] == '七' else chinese_num[day])
    else:
        week = '假期时间'
    return api_response(
        {
            'menu': menu,
            'person_info': person_info,
            'mini_schedule': intelligent_recommendation(person),
            'wx_info': wx_info,
            'week': week,
            'morning': {
                'is_morning_sign': is_morning_sign(user),
                'morning_stop_hour': 23,
                'morning_stop_minute': 59,
                'morning_start_hour': 5,
                'morning_start_minute': 59
            },
            'welcome': get_welcome(person),
        }
    )
