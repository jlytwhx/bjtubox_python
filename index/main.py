import datetime
from django.forms.models import model_to_dict
from freeclass.models import Classroom
from schedule.main import get_full_kcb


def get_menu_list(person):
    applications = person.group.applications.all()
    return [model_to_dict(x) for x in applications]


def get_welcome(person):
    person_type = '老师' if person.group.id == 0 else '同学'
    # if datetime.datetime.now().strftime("%m%d") == person.id_card[10:14]:
    #     return '生日快乐！' + person.name + person_type
    now = datetime.datetime.now()
    hour = int(now.hour)
    if 4 < hour < 9:
        tip = '早上好!'
    elif 9 <= hour < 11:
        tip = '上午好！'
    elif 11 <= hour < 13:
        tip = '中午好!'
    elif 13 <= hour < 18:
        tip = '下午好!'
    elif 18 <= hour < 23:
        tip = '晚上好'
    else:
        tip = '早点儿休息吧！'
    return tip + '  ' + person.name + person_type
