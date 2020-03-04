import requests
import time
import json
import hashlib
from django.http import HttpResponse
from django.shortcuts import render
from .models import Follow
from urllib.parse import quote
from django.http import HttpResponseRedirect
from main import api_response

# Create your views here.
AppID = ''
APPSecret = ''


def get_access_token():
    api = 'https://api.weixin.qq.com/cgi-bin/token'
    params = {
        'grant_type': 'client_credential',
        'appid': AppID,
        'secret': APPSecret
    }
    response = requests.get(url=api, params=params).json(encoding='utf-8')
    token = response['access_token']
    return token


def get_user_access_token_and_openid(code):
    api = 'https://api.weixin.qq.com/sns/oauth2/access_token'
    params = {
        'appid': AppID,
        'secret': APPSecret,
        'code': code,
        'grant_type': 'authorization_code'
    }
    response = requests.get(api, params=params).json(encoding='utf-8')
    openid = response['openid']
    access_token = response['access_token']
    return openid, access_token


def get_user_info(code):
    openid, access_token = get_user_access_token_and_openid(code)
    api = 'https://api.weixin.qq.com/sns/userinfo'
    params = {
        'access_token': access_token,
        'openid': openid,
        'lang': 'zh_CN'
    }
    content = requests.get(api, params=params).content.decode()
    response = json.loads(content)
    nickname = response['nickname']
    avatar_url = response['headimgurl']
    return openid, nickname, avatar_url


def get_ticket():
    api = 'https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token={}&type=jsapi'.format(get_access_token())
    response = requests.get(url=api).json(encoding='utf-8')
    ticket = response['ticket']
    return ticket


def get_signature(timestamp, ticket, nonce_str, url):
    data = {
        'timestamp': timestamp,
        'url': url,
        'jsapi_ticket': ticket,
        'noncestr': nonce_str
    }
    string = '&'.join(['{}={}'.format(key, data[key]) for key in sorted(list(data.keys()))])
    sha1 = hashlib.sha1()
    sha1.update(string.encode())
    signature = sha1.hexdigest()
    return signature, string


def verify(request):
    return HttpResponse("SGglzEfQCwUCafws")


def goto_tuisong(request):
    url = 'https://mp.weixin.qq.com/s/5Pq9e86FXO2hh1IbkPT8jA'
    return render(request, 'sports.html', {'url': url})


def introduce(request):
    try:
        code = request.GET['code']
        openid, nickname, avatar = get_user_info(code)
    except:
        url = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid=&redirect_uri={}&' \
              'response_type=code&scope=snsapi_userinfo&state=STATE#wechat_redirect'.format(
            quote('https://mp.bjtu.edu.cn/guanwei/introduce/'))
        return HttpResponseRedirect(url)
    f = Follow.objects.get_or_create(nickname=nickname, openid=openid)[0]
    timestamp = str(int(time.time()))
    ticket = get_ticket()
    context = {
        'app_id': AppID,
        'timestamp': timestamp,
        'nonce_str': timestamp,
        'nickname': nickname,
        'avatar': avatar,
        'signature': get_signature(timestamp, ticket, timestamp,
                                   'https://mp.bjtu.edu.cn/guanwei/introduce/?code={}&state={}'.format(
                                       code, 'STATE'
                                   ))[0],
        'num': f.id,
        'string': get_signature(timestamp, ticket, timestamp,
                                'https://mp.bjtu.edu.cn/guanwei/introduce/?code={}&state={}'.format(
                                    code, 'STATE'
                                ))[1]
    }
    return render(request, 'introduce.html', context=context)


def get_wx_url():
    url = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid=&redirect_uri={}&' \
          'response_type=code&scope=snsapi_userinfo&state=STATE#wechat_redirect'.format(
        quote('https://mp.bjtu.edu.cn/guanwei/2020/'))
    return url


def api_guoqing(request):
    code = request.GET['code']
    openid, nickname, avatar = get_user_info(code)
    timestamp = str(int(time.time()))
    ticket = get_ticket()
    result = {
        'app_id': AppID,
        'timestamp': timestamp,
        'nonce_str': timestamp,
        'nickname': nickname,
        'avatar': avatar,
        'signature': get_signature(timestamp, ticket, timestamp,
                                   'https://mp.bjtu.edu.cn/guanwei/guoqing/index.html?code={}&state={}'.format(
                                       code, 'STATE'
                                   ))[0],
        'string': get_signature(timestamp, ticket, timestamp,
                                'https://mp.bjtu.edu.cn/guanwei/guoqing/index.html?code={}&state={}'.format(
                                    code, 'STATE'
                                ))[1]
    }
    return api_response(result)


def api_kaoyan(request):
    code = request.GET['code']
    openid, nickname, avatar = get_user_info(code)
    timestamp = str(int(time.time()))
    ticket = get_ticket()
    f = Follow.objects.get_or_create(nickname=nickname, openid=openid)[0]
    result = {
        'app_id': AppID,
        'timestamp': timestamp,
        'nonce_str': timestamp,
        'nickname': nickname,
        'avatar': avatar,
        'num': f.id,
        'signature': get_signature(timestamp, ticket, timestamp,
                                   'https://mp.bjtu.edu.cn/guanwei/kaoyan/?code={}&state={}'.format(
                                       code, 'STATE'
                                   ))[0],
        'string': get_signature(timestamp, ticket, timestamp,
                                'https://mp.bjtu.edu.cn/guanwei/kaoyan/?code={}&state={}'.format(
                                    code, 'STATE'
                                ))[1]
    }
    return api_response(result)


def kaoyan(request):
    return HttpResponseRedirect(get_wx_url())


if __name__ == '__main__':
    print(get_wx_url())
