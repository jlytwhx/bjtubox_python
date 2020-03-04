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


def get_point(userid):
    token = get_token()
    api = ''.format(
        userid, token)
    scores = dict()
    data = requests.get(api).json(encoding='utf-8')
    point_list = reversed(data['scores'])
    ave_point = data['pjcj']
    ave_gpa = data['pjjd']
    for point in point_list:
        xnxqmc = point['xnxqmc'].replace('\n', '')
        name = point['kcm']
        if xnxqmc not in scores:
            scores[xnxqmc] = dict()
        scores[xnxqmc][name] = point
    result = {
        'point': ave_point,
        'gpa': ave_gpa,
        'scores': scores
    }
    return result


def test_api(token):
    url = ''
    params = {
        'token': token,
    }
    response = requests.get(url, params=params)
    content = response.content.decode()
    print(response.status_code)
    print(content)


if __name__ == "__main__":
    token = get_token()
    print(token)
    test_api(token)
