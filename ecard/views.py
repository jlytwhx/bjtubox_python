# -*- coding:utf-8 -*-
from ecard import get_ecard_balance, get_ecard_record, get_month_data
from main import api_response
from user.auth import check
from user.models import User


@check
def get_user_ecard_balance(request):
    userid = request.user.person.id
    return api_response({'balance': get_ecard_balance(userid)})


@check
def get_user_ecard_records(request):
    userid = request.user.person.id
    return api_response(
        {'data': get_ecard_record(userid, num=5), 'balance': get_ecard_balance(userid)}
    )


@check
def get_month_records(request):
    userid = request.user.person.id
    month = request.GET['month']
    if month:
        month = month.replace('-', '')
    category = request.GET['category']
    result = get_month_data(userid, month, category)
    return api_response({'data': result})


@check
def get_category_list(request):
    category_list = ['图书馆支出',
                     '自助文印',
                     'MS Office',
                     '一卡通购电',
                     '医疗支出',
                     '城市热点扣费',
                     '城市热点开户',
                     '商场购物',
                     '终端取款',
                     '淋浴支出',
                     '网络扣费',
                     '上机支出',
                     '餐费支出',
                     '购热水支出',
                     'PC取款',
                     '一卡通捐赠',
                     '转帐划帐',
                     '四六级消费支出']
    return api_response({'category_list': category_list})
