import datetime

from .models import Morning, MorningContinuity, MorningSum


def is_morning_sign(user):
    return bool(Morning.objects.filter(user=user, date=datetime.datetime.now()))


def sign(user):
    is_sign_in = Morning.objects.filter(user=user, date=datetime.datetime.now())
    yesterday = Morning.objects.filter(user=user, date=datetime.datetime.now() - datetime.timedelta(days=1))
    continuity = MorningContinuity.objects.get_or_create(user=user)
    sum_day = MorningSum.objects.get_or_create(user=user)
    if not is_sign_in:
        if yesterday:
            continuity_days = continuity[0].days + 1
            continuity[0].days = continuity_days
            continuity[0].save()
        else:
            continuity[0].days = 1
            continuity[0].save()
        rank = Morning.objects.filter(date=datetime.datetime.now()).count() + 1
        sum_day[0].days = sum_day[0].days + 1
        sum_day[0].save()
        m = Morning(user=user, rank=rank)
        m.save()
        get_up_time = m.time.strftime("%H:%M:%S")
    else:
        rank = is_sign_in[0].rank
        get_up_time = Morning.objects.get(user=user, date=datetime.datetime.now()).time.strftime("%H:%M")
    return get_up_time, rank, continuity[0].days, sum_day[0].days


def get_continuity_rank(user):
    user_continuity_days = MorningContinuity.objects.get(user=user).days
    rank = MorningContinuity.objects.filter(days__gte=user_continuity_days).count()
    return rank


def get_sum_rank(user):
    user_sum_days = MorningContinuity.objects.get(user=user).days
    rank = MorningContinuity.objects.filter(days__gte=user_sum_days).count()
    return rank


def get_continuity_list():
    result = []
    continuity_list = MorningContinuity.objects.all().order_by('-days')[:20]
    for rank, person in enumerate(continuity_list):
        result.append({'rank': rank + 1,
                       'name': person.user.person.name,
                       'school': person.user.person.school,
                       'days': person.days,
                       'avatar': person.user.avatar})
    return result


def get_rank_list():
    result = []
    continuity_list = Morning.objects.filter(date=datetime.datetime.now()).order_by('rank')[:20]
    for person in continuity_list:
        result.append({'rank': person.rank,
                       'name': person.user.person.name,
                       'school': person.user.person.school,
                       'days': person.time.strftime("%H:%M"),
                       'avatar': person.user.avatar})
    return result


def get_sum_list():
    result = []
    continuity_list = MorningSum.objects.all().order_by('-days')[:20]
    for rank, person in enumerate(continuity_list):
        result.append({
            'rank': rank + 1,
            'name': person.user.person.name,
            'school': person.user.person.school,
            'days': person.days,
            'avatar': person.user.avatar})
    return result
