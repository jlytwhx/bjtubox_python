from django.db import models
from person.models import Person


# Create your models here.
class CetIdCookies(models.Model):
    person = models.OneToOneField(Person, on_delete=models.CASCADE)
    cookies = models.TextField(null=True)
    number = models.CharField(max_length=50, null=True, default='')
