# -*- coding:utf-8 -*-
from hashlib import md5
import re
from main import error
from django.core.cache import cache
from user.models import User
import time
from urllib.parse import parse_qs


def check_without_login(func):
    def wrapper(request):
        if 'HTTP_TOKEN' in request.META:
            token = request.META['HTTP_TOKEN']
            if token in cache:
                # 敏感代码
                if sign.lower() != real_sign.lower():
                    return error(2011)  # 签名无效
                elif time.time() - int(params['ts']) > 180:
                    return error(2012)  # 签名过期
                else:
                    user = User.objects.get(openid=openid)
                    request.user = user
                    return func(request)
            else:
                return error(2001)  # token无效或token已过期
        else:
            return error(2002)  # 无token

    return wrapper


def check(func):
    def wrapper(request):
        if 'HTTP_TOKEN' in request.META:
            token = request.META['HTTP_TOKEN']
            if token in cache:
                # 敏感代码
                if sign.lower() != real_sign.lower():
                    return error(2011)  # 签名无效
                elif time.time() - int(params['ts']) > 180:
                    return error(2012)  # 签名过期
                else:
                    user = User.objects.get(openid=openid)
                    if not user.person:
                        return error(2003)
                    request.user = user
                    return func(request)
            else:
                return error(2001)  # token无效或token已过期
        else:
            return error(2002)  # 无token

    return wrapper


def get_user_by_token(token):
    openid, code = cache.get(token).split('|')
    user = User.objects.get(openid=openid)
    return user
