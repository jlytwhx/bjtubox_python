# chat/consumers.py
from asgiref.sync import async_to_sync
from user.models import User
from .models import Message, ChatRoom
from channels.generic.websocket import WebsocketConsumer
from django.core.cache import cache
from .main import online_list, recent_message
import json
import hashlib
import datetime


class ChatConsumer(WebsocketConsumer):
    user = None
    code = None

    def auth(self):
        token = [header[1].decode() for header in self.scope['headers'] if header[0].decode() == 'token'][0]
        print(token, type(token))
        openid, code = cache.get(token).split('|')
        user = User.objects.get(openid=openid)
        self.user = user
        self.code = code

    def check_signature(self, message, signature):
        string = "code={}&message={}".format(self.code, message)
        md5 = hashlib.md5()
        md5.update(string.encode())
        real_signature = md5.hexdigest()
        return real_signature.lower() == signature.lower()

    def connect(self):
        self.auth()
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        cache.set("room_{}_{}".format(self.room_name, self.user.person_id),
                  self.user.avatar + '|||' + self.user.nickname, None)
        self.accept()
        data = {
            'type': 'base_info',
            'room_name': ChatRoom.objects.get(id=self.room_name).name,
            'person_id': self.user.person_id
        }
        self.send(text_data=json.dumps(data, ensure_ascii=False))
        data = {
            'type': 'online_list',
            'data': online_list(self.room_name)
        }
        self.send(text_data=json.dumps(data, ensure_ascii=False))
        data = {
            'type': 'history',
            'data': recent_message(self.room_name)
        }
        self.send(text_data=json.dumps(data, ensure_ascii=False))
        data = {
            'type': 'online',
            'person_id': self.user.person_id,
            'avatar_url': self.user.avatar,
            'nickname': self.user.nickname,
            'content': "{}上线了！".format(self.user.nickname)
        }
        self.send_group_message(json.dumps(data, ensure_ascii=False))

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
        cache.delete("room_{}_{}".format(self.room_name, self.user.person_id))
        data = {
            'type': 'offline',
            'person_id': self.user.person_id,
            'content': "{}下线了！".format(self.user.nickname)
        }
        self.send_group_message(json.dumps(data, ensure_ascii=False))

    # Receive message from WebSocket
    def send_group_message(self, message):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['content']
        message_type = text_data_json['type']
        new_message = Message(person_id=self.user.person_id, content=message, room_id=self.room_name, type=message_type)
        new_message.save()
        json_message = json.dumps({
            ('content' if message_type == 'text' else 'image_url'): message if message_type == 'text' else (
                    "https://mp.bjtu.edu.cn/file/user/image/" + message),
            'time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'person_id': self.user.person_id,
            'nickname': self.user.nickname or '没有填写名字',
            'avatar_url': self.user.avatar,
            'type': message_type
        }, ensure_ascii=False)
        # Send message to room group
        self.send_group_message(json_message)

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        # Send message to WebSocket
        self.send(text_data=message)
