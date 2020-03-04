from django.db import models


# Create your models here.
class Follow(models.Model):
    openid = models.CharField(max_length=50)
    nickname = models.CharField(max_length=100)
    time = models.DateTimeField(auto_now_add=True)
