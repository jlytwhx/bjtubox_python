from django.db import models


# Create your models here.
class Application(models.Model):
    text = models.CharField(max_length=20)
    url = models.CharField(max_length=50)
    icon = models.CharField(max_length=50)

    def __str__(self):
        return self.text
