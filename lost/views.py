# -*- coding:utf-8 -*-
from main import send_message, api_response, error
from lost.models import Lost, Comment
from user.auth import check
from person.models import Person
import uuid
import json
from .main import get_comment
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from urllib.parse import parse_qs


@csrf_exempt
@check
def comment(request):
    if request.method == 'GET':
        lost_id = request.GET['lost_id']
        result = get_comment(lost_id, request.user)
        return api_response({'data': result})

    elif request.method == 'POST':
        lost_id = request.POST['lost_id']
        content = request.POST['content']
        at = request.POST['at'] if 'at' in request.POST else None
        if at:
            send_message(at, '{}在失物招领中评论你了!【{}】'.format(request.user.person.name, content))
        image = request.POST['image'] if 'image' in request.POST else None
        comment_id = str(uuid.uuid4())
        new = Comment.objects.create(id=comment_id, openid=request.user, content=content, at=at, image=image,
                                     lost_id=Lost.objects.get(id=lost_id))
        new.save()
        return api_response({'msg': '评论成功！', 'comment_id': comment_id})

    elif request.method == 'DELETE':
        comment_id = parse_qs(request.body.decode())['comment_id'][0]
        comment_object = Comment.objects.get(id=comment_id)
        if comment_object.openid.openid == request.user.openid:
            comment_object.delete()
            return api_response({'msg': '删除成功'})
        else:
            return error(3202)


@csrf_exempt
@check
def lost(request):
    if request.method == 'GET':
        page_size = int(request.GET['page_size'])
        page = int(request.GET['page'])
        lost_list = Lost.objects.filter(show=True).order_by('-time')[(page - 1) * page_size:(page * page_size)]
        result = []
        for info in lost_list:
            data = model_to_dict(info)
            data['name'] = info.openid.person.name
            data['avatar'] = info.openid.avatar
            data['time'] = info.time.strftime("%Y-%m-%d %H:%M:%S")
            data['id'] = str(data['id']).replace('-', '')
            data['mine'] = bool(data.pop('openid') == request.user.openid)
            data['comments'] = get_comment(info.id, request.user)

            if info.at:
                at_person = Person.objects.get(id=info.at).name
                data['at'] = "%s(%s)" % (at_person, info.at)
            else:
                data['at'] = False
            if info.image:
                data['image'] = "https://mp.bjtu.edu.cn/file/user/image/" + info.image
            else:
                data['image'] = False
            result.append(data)
        return api_response({'data': result})

    if request.method == 'POST':
        content = request.POST['content']
        lost_type = request.POST['type']
        at = request.POST['at'] if 'at' in request.POST else None
        if at:
            send_message(at, '{}在失物招领中提到了你！【{}】'.format(request.user.person.name, content))
        image = request.POST['image'] if 'image' in request.POST else None
        lost_id = str(uuid.uuid4())
        new = Lost.objects.create(id=lost_id, openid=request.user, content=content, at=at, image=image, type=lost_type)
        new.save()
        return api_response({'msg': '发送成功！', 'lost_id': lost_id})

    elif request.method == 'DELETE':
        lost_id = parse_qs(request.body.decode())['lost_id'][0]
        lost_object = Lost.objects.get(id=lost_id)
        if lost_object.openid.openid == request.user.openid:
            lost_object.delete()
            return api_response({'msg': '删除成功'})
        else:
            return error(3201)
