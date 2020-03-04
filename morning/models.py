from django.db import models
from user.models import User


# Create your models here.
class Morning(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)
    time = models.TimeField(auto_now=True)
    rank = models.IntegerField()


class MorningSum(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    days = models.IntegerField(default=0)


class MorningContinuity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    days = models.IntegerField(default=0)
