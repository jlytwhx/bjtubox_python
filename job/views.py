import time
import hashlib
import requests
from user.auth import check
from main import api_response, error

KEY = ''


# Create your views here.
@check
def login_to_bjtu_job(request):
    def sign(name, ts):
        string = f''
        md5 = hashlib.md5()
        md5.update(string.encode())
        return str(md5.hexdigest())

    user = request.user
    student_id = user.person.id
    time_stamp = int(time.time())
    signature = sign(student_id, time_stamp)
    api = ''
    data = {
        'name': student_id,
        'ts': time_stamp,
        'sn': signature
    }
    response = requests.post(api, data).json()
    if int(response['code']) == 0:
        token = response['token']
        return api_response({'token': token})
    else:
        return error(4001)
