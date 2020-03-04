from django.db import models
from person.models import Person


class Course(models.Model):
    id = models.AutoField(primary_key=True)
    course_id = models.CharField(max_length=20)
    course_no = models.SmallIntegerField()
    name = models.CharField(max_length=50)
    school = models.CharField(max_length=50)
    teacher = models.ForeignKey(Person, on_delete=models.CASCADE)
    week = models.CharField(max_length=128)
    hour = models.SmallIntegerField()
    point = models.FloatField()
    day = models.SmallIntegerField()
    day_no = models.SmallIntegerField()
    building = models.CharField(max_length=20)
    classroom = models.CharField(max_length=50)

    def __str__(self):
        return '{}-{}【{}[{}]】'.format(self.name, self.teacher.name, self.course_id, self.course_no)
