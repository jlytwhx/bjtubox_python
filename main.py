# -*- coding:utf-8 -*-
import json
import time
import base64
import requests
from Crypto.Cipher import AES
from django.http import HttpResponse

app_id = ''
app_secret = ''
corp_id = ''
corp_secret = ''


def error(code):
    error_dict = {
        '2001': 'Token无效或已过期',
        '2002': '无Token',
        '2003': '需要绑定学号',
        '2010': '无签名',
        '2011': '签名无效',
        '2012': '签名已过期',
        '3001': '请检查是否输入了错误的学工号或未在企业号上注册',
        '3002': '验证码输入错误，或验证码已过期',
        '3101': 'session_id不在用户已登录设备列表中',
        '3201': '无权删除此人失物招领',
        '3202': '无权删除此人评论',
        '3203': '失物招领&寻物启事不存在',
        '3301': '无权删除此贺卡',
        '3302': '贺卡不存在',
        '3401': '查询失败，请检查验证码是否输入错误',
        '3501': '打卡失败，你今日已经打过卡了！',
        '4001': '登录就业系统失败!'
    }
    return HttpResponse(json.dumps({'code': int(code), 'msg': error_dict[str(code)]}, ensure_ascii=False))


def api_response(data):
    result = {
        'code': 0,
        'msg': '成功！'
    }
    result.update(data)
    return HttpResponse(json.dumps(result, ensure_ascii=False))


def get_wx_avatar(userid):
    api = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={}&corpsecret={}'.format(corp_id, corp_secret)
    access_token = requests.get(api, verify=False).json()['access_token']
    api = 'https://qyapi.weixin.qq.com/cgi-bin/user/get?access_token={}&userid={}'.format(access_token, userid)
    avatar = requests.get(api).json(encoding='utf-8')['avatar']
    return avatar


def send_message(userid, content):
    api = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={}&corpsecret={}'.format(corp_id, corp_secret)
    access_token = requests.get(api, verify=False).json()['access_token']
    body = json.dumps({
        "touser": userid,
        "msgtype": "text",
        "agentid": 147,
        "text": {
            "content": content
        },
        "safe": 0
    }, ensure_ascii=False).encode('utf-8')
    url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={}'.format(access_token)
    result = requests.post(url, data=body, verify=False).json()
    if result['errcode'] == 0:
        return True
    elif result['errcode'] == 82001:
        return False


def get_access_token():
    api = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}'.format(app_id,
                                                                                                           app_secret)
    response = requests.get(api).json()
    return response['access_token']


def send_template_message(openid, form_id, template_id, data: dict, page=False):
    api = 'https://api.weixin.qq.com/cgi-bin/message/wxopen/template/send?access_token={}'.format(get_access_token())
    data = {
        "touser": openid,
        "template_id": template_id,
        "form_id": form_id,
        "data": {key: {'value': value} for key, value in data.items()},
    }
    if page:
        data['page'] = page
    requests.post(api, json=data)


def wx_data_crypt(session_key, encrypted_data, iv):
    session_key = base64.b64decode(session_key)
    encrypted_data = base64.b64decode(encrypted_data)
    iv = base64.b64decode(iv)
    cipher = AES.new(session_key, AES.MODE_CBC, iv)
    data = cipher.decrypt(encrypted_data)
    data = data[:-ord(data[len(data) - 1:])].decode()
    decrypted = json.loads(data)
    if decrypted['watermark']['appid'] != app_id:
        raise Exception('Invalid Buffer')
    return decrypted


def get_now_week():
    week = (int(time.time()) - 1567353600) // (7 * 24 * 3600) or 1
    return week


if __name__ == '__main__':
    print(get_now_week())
