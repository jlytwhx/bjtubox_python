# -*- coding:utf-8 -*-
from sport.models import Sport


def get_rank_list(date, school=None):
    result = []
    search_dict = {'date': date}
    if school:
        search_dict['school'] = school
    day_list = Sport.objects.filter(**search_dict).order_by('-step')[0:10]
    for i in range(len(day_list)):
        day = day_list[i]
        user = day.user
        person = user.person
        result.append(
            {'name': person.name, 'school': person.school, 'class': person.stu_class, 'rank': i + 1, 'step': day.step,
             'avatar': user.avatar})
    return result


def get_rank(date, user):
    step = int(Sport.objects.get(date=date, user=user).step)
    school_rank = Sport.objects.filter(date=date, step__gt=step, school=user.person.school).count() + 1
    all_rank = Sport.objects.filter(date=date, step__gt=step).count() + 1
    return school_rank, all_rank
