from urllib.parse import unquote
import requests
from bs4 import BeautifulSoup


class Dean:
    _mis_user = ''
    _mis_password = ''
    _is_mis_login = False
    _is_dean_login = False

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit'
                                                   '/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'})

    def mis_session(self):
        login_api = 'https://mis.bjtu.edu.cn'
        response = self.session.get(login_api)
        content = response.content.decode()
        uri = response.url
        csrf = BeautifulSoup(content, 'html5lib').find('input', {'name': 'csrfmiddlewaretoken'}).get('value')
        data = {
            'next': unquote(uri.replace('https://cas.bjtu.edu.cn/auth/login/?next=', '')),
            'csrfmiddlewaretoken': csrf,
            'loginname': self._mis_user,
            'password': self._mis_password
        }
        self.session.headers.update({
            'Referer': 'https://cas.bjtu.edu.cn/auth/login/',
            'Upgrade-Insecure-Requests': '1'
        })
        self.session.post(uri, data).content.decode()
        self._is_mis_login = True
        return self.session

    @property
    def dean_session(self):
        if not self._is_mis_login:
            self.mis_session()
        url = 'https://mis.bjtu.edu.cn/module/module/10/'
        content = self.session.get(url).content.decode()
        next_url = BeautifulSoup(content, 'html5lib').find('form').get('action')
        self.session.get(next_url).content.decode()
        return self.session
