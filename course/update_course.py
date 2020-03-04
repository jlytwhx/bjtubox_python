import requests


def get_token():
    api = ''
    data = {
        'loginname': '',
        'password': ''
    }
    data = requests.post(api, data).json(encoding='utf-8')
    token = data['token']
    return token


def get_course(token):
    api = ''
    params = {
        'token': token
    }
    content = requests.get(api, params=params).content.decode()
    print(content)


if __name__ == '__main__':
    token = get_token()
    print(token)
