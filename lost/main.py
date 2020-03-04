from lost.models import Lost, Comment
from user.models import User
from django.forms import model_to_dict


def get_comment(lost_id, user):
    comment_list = Lost.objects.get(id=lost_id).comment_set.all()
    if not comment_list:
        return []
    result = []
    for info in comment_list:
        if info.show:
            data = model_to_dict(info)
            data['time'] = info.time.strftime("%Y-%m-%d %H:%M:%S")
            data['id'] = str(data['id']).replace('-', '')
            data['lost_id'] = str(data['lost_id']).replace('-', '')
            data['name'] = info.openid.person.name
            data['mine'] = bool(data.pop('openid') == user.openid)
            result.append(data)
    return result
