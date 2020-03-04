from django.db import models
from person.models import Person


class Schedule(models.Model):
    student = models.ForeignKey(Person, on_delete=models.CASCADE)
    course_id = models.CharField(max_length=20)
    course_no = models.IntegerField()
