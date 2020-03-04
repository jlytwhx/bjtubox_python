# -*- coding:utf-8 -*-
import time
import json
import base64
import requests

api = ''


def get_network_base_info(userid):
    base64_query = base64.b64encode(''.format(userid).encode()).decode()
    url = api + base64_query
    data = requests.get(url).json(encoding='utf-8')['list']
    if not data:
        return False
    data = data[0]
    account = data['account']
    use_flow = data['useflow']
    carry_over_flow = data['carryoverflow']
    package_flow = data['packageflow']
    balance = data['balance']
    limit_money = data['limitmoney']
    result = {
        'account': account,
        'use_flow': use_flow,
        'carry_over_flow': carry_over_flow,
        'package_flow': package_flow,
        'balance': balance,
        'limit_money': limit_money
    }
    return result


def get_online_list(userid):
    result = []
    base64_query = base64.b64encode(''.format(userid).encode()).decode()
    url = api + base64_query
    data = requests.get(url).json(encoding='utf-8')['list'] or []
    for device in data:
        login_ip = device['loginip']
        session_id = device['sessionid']
        login_time = device['logintime']
        login_mac = device['loginmac']
        device_type = device['devicetype']
        result.append({
            'ip': login_ip,
            'mac': login_mac,
            'time': login_time,
            'session_id': session_id,
            'type': device_type}
        )
    return result


def offline_device(account, session_id):
    url = ''
    params = {
        'c': 'ServiceInterface',
        'a': 'offlineUserDevice',
        'account': account,
        'sessionid': session_id,
        '_': int(time.time())
    }
    try:
        content = requests.get(url, params).content.decode('gbk')
        data = json.loads(content[1:-1])
        return data['result'] == 'ok'
    except:
        return False


if __name__ == '__main__':
    offline_device('16211268', '20611')
