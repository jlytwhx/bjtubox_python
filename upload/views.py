# -*- coding:utf-8 -*-
from django.views.decorators.csrf import csrf_exempt
from main import api_response
import os
import uuid


# Create your views here.

@csrf_exempt
def upload_image(request):
    image = request.FILES.get("file", None)  # 获取上传的文件，如果没有文件，则默认为None
    name = str(uuid.uuid4())
    file_type = image.name.split('.')[-1]
    destination = open(os.path.join("/home/ubuntu/file/user/image/", name + '.' + file_type), 'wb+')  # 打开特定的文件进行二进制的写操作
    for chunk in image.chunks():  # 分块写入文件
        destination.write(chunk)
    destination.close()
    return api_response({
        "msg": "upload successful!",
        "filename": "%s.%s" % (name, file_type)
    })
