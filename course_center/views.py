import json
import requests
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from urllib.parse import urlencode, quote
from user.auth import check
from main import api_response
from django.http import HttpResponseServerError


@check
def cc_session(request):
    return api_response({'session': '56F7DF5F070E020A9CA8EE0D163351F4.TE1'})


@csrf_exempt
def down_file(request, *args, **kwargs):
    method = request.method
    url = request.get_raw_uri()
    url = url.replace(url.split('/cc/jump/file/')[0], '').replace('/cc/jump/file/', '')
    session = url.split('/')[0]
    file_id: str = url[url.index('id=') + 3:]
    url = url.replace(file_id, file_id.upper())
    url = 'http://cc.bjtu.edu.cn:81/meol' + url.replace(session, '')
    content = requests.get(url, headers={
        'cookie': 'JESESSIONID={}'.format(session)
    }).content
    return HttpResponse(content)


@csrf_exempt
def jump(request, *args, **kwargs):
    method = request.method
    url = request.get_raw_uri()
    url = url.replace(url.split('/cc/jump/')[0], 'http://cc.bjtu.edu.cn:81/meol').replace('cc/jump/', '')
    headers = dict(request.headers)
    for key in ['Host', 'Referer', 'Content-Length']:
        if key in headers:
            del headers[key]
    if method == 'GET':
        content = requests.get(url, headers=headers)
    else:
        if 'write.do.jsp' in url:
            hwaid = request.POST['hwaid']
            hwtid = request.POST['hwtid']
            input_body = request.POST['IPT_BODY'].encode('gbk')
            data = {'hwaid': hwaid, 'hwtid': hwtid, 'IPT_BODY': input_body}
            headers.update({
                'Content-Type': 'application/x-www-form-urlencoded'
            })
            content = requests.post(url, headers=headers,
                                    data=data)
        else:
            content = requests.post(url, headers=headers, data=request.body)
    if int(content.status_code) == 200:
        return HttpResponse(content.content.decode('gbk'))
    else:
        if 'ermission' in content.content.decode('gbk'):
            return HttpResponseServerError(HttpResponse(content).content.decode('gbk'))
        else:
            return HttpResponse(content.content.decode('gbk'))
