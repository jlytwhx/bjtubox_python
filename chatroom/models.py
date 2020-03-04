from django.db import models
from person.models import Person


# Create your models here.
class ChatRoom(models.Model):
    name = models.CharField(max_length=50)


class Message(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now=True)
    type = models.CharField(max_length=10)
    content = models.CharField(max_length=250, null=True)
