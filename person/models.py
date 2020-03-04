from django.db import models
from index.models import Application


class Group(models.Model):
    id = models.SmallIntegerField(primary_key=True)
    name = models.CharField(max_length=10)
    applications = models.ManyToManyField(Application)

    def __str__(self):
        return self.name


class Person(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    sex = models.CharField(max_length=4)
    name = models.CharField(max_length=30)
    school = models.CharField(max_length=30)
    profession = models.CharField(max_length=40)
    stu_class = models.CharField(max_length=30)
    province = models.CharField(max_length=20)
    nation = models.CharField(max_length=10)
    grade = models.IntegerField()
    phone = models.CharField(max_length=20)
    id_card = models.CharField(max_length=30, null=True)
    email = models.CharField(max_length=100, null=True)
    group = models.ForeignKey(Group, on_delete=None)

    def __str__(self):
        return self.name + '-' + self.id
