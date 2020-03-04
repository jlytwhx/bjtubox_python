from user.auth import get_user_by_token, check
from .main import PersonData
from .models import BigData
from user.models import User
from django.shortcuts import render
from main import api_response
import datetime
import json


@check
def status(reqeust):
    return api_response({'msg': 'ok'})


def index(request):
    user = User.objects.get(openid='o9blN5ZAEhbOjRRvfB6xCsowfrio')
    person_save_data = user.person.bigdata_set.all()[0]
    part_data = sorted([
        {'name': '淋浴', 'value': person_save_data.shower_cost},
        {'name': '餐费', 'value': person_save_data.eat_cost},
        {'name': '购电', 'value': person_save_data.electric_cost},
        {'name': '上机', 'value': person_save_data.computer_cost},
        {'name': '购物', 'value': person_save_data.shop_cost},
        {'name': '热水', 'value': person_save_data.water_cost},
        {'name': '医疗', 'value': person_save_data.hospital_cost},
    ], key=lambda x: x['value'])
    return render(request, 'index.html',
                  {'name': user.person.name, 'part_data': json.dumps(part_data, ensure_ascii=False)})
# def index(request):
#     token = request.GET['token']
#     user = get_user_by_token(token)
#     avatar = user.avatar
#     person_save_data = user.person.bigdata_set.all()[0]
#     p = PersonData(user.person_id)
#     p.load_data()
#     p.get_lost_card_data()
#     p.get_most_like_department()
#     shop_list = sorted([[data[0], data[1]] for data in p.department_data if data[3] == '商场购物'], key=lambda x: x[1],
#                        reverse=True)[:5]
#     shop_dict = {p[0]: p[1] for p in shop_list}
#     restaurant_list = sorted([[data[0], data[1]] for data in p.department_data if data[3] == '餐费支出'],
#                              key=lambda x: x[1], reverse=True)[:5]
#     restaurant_dict = {p[0]: p[1] for p in restaurant_list}
#     result = {
#         'shop_data': shop_dict,
#         'restaurant_data': restaurant_dict,
#         'engel': person_save_data.engel_num,
#         'part_data': sorted([
#             {'name': '淋浴', 'value': person_save_data.shower_cost},
#             {'name': '餐费', 'value': person_save_data.eat_cost},
#             {'name': '购电', 'value': person_save_data.electric_cost},
#             {'name': '上机', 'value': person_save_data.computer_cost},
#             {'name': '购物', 'value': person_save_data.shop_cost},
#             {'name': '热水', 'value': person_save_data.water_cost},
#             {'name': '医疗', 'value': person_save_data.hospital_cost},
#         ], key=lambda x: x['value']),
#         'first_ill_time': False if not person_save_data.first_ill_time else person_save_data.first_ill_time.strftime(
#             "%Y-%m-%d"),
#         'lost_card_num': person_save_data.lost_card_num,
#         'lost_card_min': (person_save_data.lost_card_min // (3600 * 24) if person_save_data.lost_card_min > 0 else None)
#     }
#     lost_card_date = False
#     lost_card_min = False
#     if result['lost_card_num'] > 0:
#         min_second = float('inf')
#         for i in range(len(p.lost_card_data) - 1):
#             if p.lost_card_data[i + 1]['lost_timestamp'] - p.lost_card_data[i]['lost_timestamp'] < min_second:
#                 lost_card_date = datetime.datetime.fromtimestamp(p.lost_card_data[i]['lost_timestamp']).strftime(
#                     "%Y年%m月%d日")
#                 min_second = (p.lost_card_data[i + 1]['lost_timestamp'] - p.lost_card_data[i]['lost_timestamp']) // (
#                         3600 * 24)
#                 lost_card_min = (p.lost_card_data[i + 1]['lost_timestamp'] - p.lost_card_data[i]['lost_timestamp']) // (
#                         3600 * 24)
#     lost_card_percent = int(BigData.objects.filter(
#         lost_card_num__lt=person_save_data.lost_card_num).count() / BigData.objects.count() * 100)
#     result = {k: json.dumps(v, ensure_ascii=False) for k, v in result.items()}
#     return render(request, "datashow.html",
#                   {'name': user.person.name, 'avatar': avatar, 'part_data': result['part_data'],
#                    'shop_data': result['shop_data'],
#                    'restaurant_data': result['restaurant_data'], 'engel': int(float(result['engel']) * 100),
#                    'first_ill_time': result['first_ill_time'], 'lost_card_date': lost_card_date,
#                    'lost_card_min_day': lost_card_min, 'lost_card_num': person_save_data.lost_card_num - 1,
#                    'lost_card_percent': lost_card_percent})
