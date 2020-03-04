import json
from django.http import HttpResponse
from person.models import Person
from point.main import get_point
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
def response(information):
    data = {
        'code': 0
    }
    data.update(information)
    return HttpResponse(json.dumps(data, ensure_ascii=False))


def fail_response(err_msg):
    data = {
        'code': 1,
        'msg': err_msg
    }
    return HttpResponse(json.dumps(data, ensure_ascii=False))


@csrf_exempt
def api_point(request):
    user_id = request.POST['user_id']
    password = request.POST['password']
    person = Person.objects.filter(id=user_id, id_card=password)
    if not person:
        return fail_response('用户名或密码错误！')
    point = get_point(user_id)
    score = point['scores']
    last = score[list(score.keys())[0]]
    result = []
    for k, v in last.items():
        name = k
        point = v['kccj']
        voice = f'你的{name}成绩是,{point}。'
        result.append(voice)
    return response({'point': ''.join(result)})
