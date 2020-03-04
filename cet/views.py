from user.auth import check
from .main import cet_number, verify_code
from django.http import HttpResponse
from main import api_response, error
from .models import CetIdCookies


@check
def get_verify_code(request):
    person = request.user.person
    score = CetIdCookies.objects.filter(person=person)
    if score and score[0].number:
        return api_response({
            'data': {
                'number': score[0].number,
                'name': person.name,
                'type': 'CET4' if int(str(score[0].number)[9]) == 1 else 'CET6'

            }
        })
    return api_response({
        'image': verify_code(person),
        'data': False
    })


@check
def get_cet_number(request):
    person = request.user.person
    code = request.GET['verifyCode']
    number = cet_number(person, code)
    if number and type(number) == int:
        return api_response({
            'msg': '查询成功！',
            'data': {
                'number': number,
                'name': person.name,
                'type': 'CET4' if int(str(number)[9]) == 1 else 'CET6'
            }
        })
    else:
        return api_response({
            'msg': number,
            'code': 3401
        })
