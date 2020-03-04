from django.db import models
from django.contrib.auth.models import AbstractUser
from person.models import Person


# Create your models here.
# models.py

class User(models.Model):
    openid = models.CharField(max_length=32, primary_key=True)
    person = models.ForeignKey(Person, on_delete=models.CASCADE, null=True)
    session_key = models.CharField(max_length=24, null=True)
    nickname = models.CharField(max_length=30, null=True)
    city = models.CharField(max_length=32, null=True)
    avatar = models.CharField(max_length=256, null=True)
    register_time = models.DateTimeField(auto_now_add=True)
    last_login_time = models.DateTimeField(auto_now=True, null=True)
    token = models.CharField(max_length=32, null=True)

    def __unicode__(self):
        return self.openid + self.person.name
