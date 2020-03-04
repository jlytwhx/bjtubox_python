from django.db import models
from user.models import User


# Create your models here.
class Sport(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    step = models.IntegerField()
    school = models.CharField(max_length=32)

