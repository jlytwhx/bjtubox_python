# -*- coding:utf-8 -*-
import requests
import json
import random
from main import app_id, app_secret, api_response, send_message, error, wx_data_crypt, get_wx_avatar
from user.models import User
from user.auth import check, check_without_login
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache
import uuid
from person.models import Person


def login(request):
    code = request.GET['code']
    url = 'https://api.weixin.qq.com/sns/jscode2session'
    data = {
        'appid': app_id,
        'secret': app_secret,
        'js_code': code,
        'grant_type': 'authorization_code'
    }
    info = json.loads(requests.get(url, data).content.decode())
    openid = info['openid']
    session_key = info['session_key']
    token = str(uuid.uuid4()).replace('-', '')
    person, _ = User.objects.get_or_create(openid=openid)
    person.session_key = session_key
    cache.set(token, openid + '|' + code, 2 * 60 * 60)
    person.save()
    return api_response({'msg': '登陆成功!', 'token': token, 'register': bool(person.person)})


@check_without_login
def get_verify_code(request):
    userid = request.GET['userid']
    user = request.user
    verify_code = random.randint(100000, 999999)
    cache.set(user.openid + '_' + userid, str(verify_code), 5 * 60)
    cache.set('111', '111', 5 * 30)
    if send_message(userid, '您的验证码为【%d】' % verify_code):
        return api_response({'msg': '发送成功！'})
    else:
        return error(3001)  # 学号输入错误


@csrf_exempt
@check_without_login
def verify(request):
    userid = request.POST['userid']
    verify_code = request.POST['verify_code']
    user = request.user
    if user.openid + '_' + userid in cache and cache.get(user.openid + '_' + userid) == str(verify_code):
        avatar = get_wx_avatar(userid)
        user.avatar = avatar
        user.person = Person.objects.get(id=userid)
        user.save()
        return api_response({'msg': '绑定成功！'})

    else:
        return error(3002)  # 验证码错误


@check
def logout(request):
    request.user.delete()
    return api_response({'msg': '注销成功！'})


@csrf_exempt
@check
def upload_user_info(request):
    session_key = request.user.session_key
    encrypted_data = request.POST['encrypted_data']
    iv = request.POST['iv']
    info = wx_data_crypt(session_key, encrypted_data, iv)
    if info:
        request.user.nickname = info['nickName']
        request.user.city = info['province'] + '_' + info['city']
        request.user.avatar = info['avatarUrl']
        request.user.save()
    return api_response({'msg': '上传成功！'})
