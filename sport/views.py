import time
from user.auth import check
from sport.models import Sport
from main import wx_data_crypt, api_response
from .main import get_rank, get_rank_list
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
@check
def upload_data(request):
    user = request.user
    person = user.person
    session_key = user.session_key
    iv = request.POST['iv']
    encrypted_data = request.POST['encryptedData']
    sports_info_list = wx_data_crypt(session_key, encrypted_data, iv)['stepInfoList']
    for day in sports_info_list[-5:]:
        step = day['step']
        date = time.strftime("%Y-%m-%d", time.localtime(day['timestamp']))
        day_info, _ = Sport.objects.get_or_create(user=user, date=date, defaults={'step': step})
        day_info.step = step
        day_info.school = person.school
        day_info.save()
    now = time.strftime("%Y-%m-%d", time.localtime(time.time()))
    school_rank, all_rank = get_rank(now, user)
    school_rank_list = get_rank_list(now, person.school)
    all_rank_list = get_rank_list(now)
    return api_response({'school_rank': school_rank, 'all_rank': all_rank, 'step': sports_info_list[-1]['step'],
                         'school_rank_list': school_rank_list, 'all_rank_list': all_rank_list,
                         'school': person.school, 'name': person.name, 'avatar': user.avatar})
