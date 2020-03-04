# -*- coding:utf-8 -*-
from main import send_message, api_response, error
from .models import Tree
from user.auth import check
import uuid
import json
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
@check
def tree(request):
    if request.method == 'GET':
        page_size = int(request.GET['page_size'])
        page = int(request.GET['page'])
        tree_list = Tree.objects.all().order_by('-time')[(page - 1) * page_size:(page * page_size)]
        result = []
        for info in tree_list:
            data = dict()
            data['content'] = info.content
            data['time'] = info.time.strftime("%Y-%m-%d %H:%M:%S")
            data['id'] = str(data['id']).replace('-', '')
            data['likes_num'] = info.treelike_set().count()
            data['comment_num'] = info.comment_set.all().count()
            data['mine'] = bool(info.user.openid == request.user.openid)
            result.append(data)
        return api_response({'data': result})

    if request.method == 'POST':
        content = request.POST['content']
        tree_id = str(uuid.uuid4())
        new = Tree.objects.create(id=tree_id, user=request.user, content=content)
        new.save()
        return api_response({'msg': '发送成功！', 'tree_id': tree_id})

    elif request.method == 'DELETE':
        tree_id = json.loads(request.body).get('tree_id')
        lost_object = Tree.objects.get(id=tree_id)
        if lost_object.openid.openid == request.user.openid:
            lost_object.delete()
            return api_response({'msg': '删除成功'})
        else:
            return error(3201)


@csrf_exempt
@check
def comment(request):
    if request.method == 'GET':
        tree_id = request.GET['tree_id']
        tree = Tree.objects.get(id=tree_id)
        comment_list = tree.comment_set().all()
