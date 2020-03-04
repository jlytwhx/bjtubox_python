from main import api_response
from user.auth import check
from .main import sign, get_continuity_list, get_sum_list, get_continuity_rank, get_sum_rank, get_rank_list


@check
def sign_in(request):
    get_up_time, rank, continuity, days = sign(request.user)
    return api_response({'rank': rank, 'continuity': continuity, 'days': days})


@check
def detail(request):
    get_up_time, rank, continuity, days = sign(request.user)
    continuity_list = get_continuity_list()
    sum_list = get_sum_list()
    continuity_rank = get_continuity_rank(request.user)
    sum_rank = get_sum_rank(request.user)
    user = request.user
    person = user.person
    return api_response({
        'name': person.name,
        'school': person.school,
        'avatar': user.avatar,
        'get_up_time': get_up_time,
        'continuity_days': continuity,
        'sum_days': days,
        'sum_rank': sum_rank,
        'rank': rank,
        'continuity_rank': continuity_rank,
        'sum_list': sum_list,
        'continuity_list': continuity_list,
        'rank_list': get_rank_list()
    })
