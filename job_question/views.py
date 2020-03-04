from main import api_response, send_template_message
from urllib.parse import parse_qs
from .models import Question
from user.auth import check_without_login
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt
import datetime


@csrf_exempt
@check_without_login
def new_question(request):
    user = request.user
    params = {k: v[0] for k, v in parse_qs(request.body.decode()).items()}
    params.pop('sn')
    params.pop('ts')
    params['openid'] = user.openid
    question = Question.objects.create(**params)
    question_id = question.id
    return api_response({
        'code': 0,
        'msg': '提交成功！老师将在24小时内回复你的问题！',
        'question_id': question_id
    })


@csrf_exempt
@check_without_login
def get_question_list(request):
    params = {k: dict(request.GET)[k][0] for k in dict(request.GET)}
    params.pop('sn')
    params.pop('ts')
    limit = 30 if 'limit' not in params else int(params.pop('limit'))
    page = 0 if 'page' not in params else int(params.pop('page'))
    if 'question_status' in params:
        params['answer__isnull'] = not bool(int(params.pop('question_status')))
    if 'mine' in params:
        params.pop('mine')
        params['openid'] = request.user.openid
    questions = Question.objects.filter(**params).order_by('-time')[limit * page:limit * (page + 1)]
    result = []
    for question in questions:
        temp = model_to_dict(question)
        temp['id'] = question.id
        temp['time'] = question.time.strftime("%Y-%m-%d %H:%M:%S")
        temp.pop('openid')
        result.append(temp)
    return api_response({'data': result})


@csrf_exempt
@check_without_login
def new_answer(request):
    question_id = request.POST['question_id']
    answer = request.POST['answer']
    teacher = request.POST['teacher']
    question = Question.objects.get(id=question_id)
    question.answer = answer
    question.teacher = teacher
    question.save()
    send_template_message(openid=question.openid, form_id=question.formId,
                          template_id='-JCZijV2jQHPdzhTgiKJMv9eLKdnPwwfb-jDFXD4RX0',
                          page='/pages/job_question/myquestion',
                          data={
                              'keyword1': answer,
                              'keyword2': teacher,
                              'keyword3': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                          })
    return api_response({'msg': '回答成功！'})
