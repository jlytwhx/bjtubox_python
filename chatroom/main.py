from .models import Message
from user.models import User
from django.core.cache import cache


def recent_message(room_id):
    message_model_to_dict = lambda x: {'time': x.time.strftime("%Y-%m-%d %H:%M:%S"), 'id': x.id,
                                       (
                                           'content' if x.type == 'text' else 'image_url'): (x.content if x.type == 'text' else ("https://mp.bjtu.edu.cn/file/user/image/" + x.content)),
                                       'person_id': x.person_id,
                                       'type': x.type,
                                       'avatar_url': User.objects.filter(person_id=x.person_id)[0].avatar}
    return [message_model_to_dict(x) for x in
            reversed(Message.objects.filter(room_id=str(room_id)).order_by('-time')[:50])]


def increase_life(room_id, user):
    cache.set('room_{}_{}'.format(room_id, user.person_id), user.avatar + '|||' + user.nickname, 50)


def online_list(room_id):
    result = dict()
    online_device = [[key, cache.get(key)] for key in cache.keys('room_{}_*'.format(room_id))]
    for device in online_device:
        user_id = device[0].split('_')[-1]
        avatar_url, nickname = device[1].split('|||')
        result[user_id] = {'avatar_url': avatar_url, 'nickname': nickname}
    return result
