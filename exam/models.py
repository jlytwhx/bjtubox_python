from django.db import models
from person.models import Person
from course.models import Course


# Create your models here.
class Exam(models.Model):
    user = models.ForeignKey(Person, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    course_id = models.CharField(max_length=30)
    course_no = models.SmallIntegerField()
    time = models.CharField(max_length=40)
    place = models.CharField(max_length=30)
    type = models.CharField(max_length=20, null=True)
    comment = models.CharField(max_length=50, null=True)
    teacher = models.CharField(max_length=30, null=True)
    school = models.CharField(max_length=40, null=True)

    def __str__(self):
        return self.user.name + '-' + self.name
