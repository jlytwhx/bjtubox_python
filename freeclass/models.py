from django.db import models


# Create your models here.
class Classroom(models.Model):  # 自习室
    name = models.CharField(max_length=30)  # 名称
    building = models.CharField(max_length=30)
    class1 = models.CharField(max_length=40)
    class2 = models.CharField(max_length=40)
    class3 = models.CharField(max_length=40)
    class4 = models.CharField(max_length=40)
    class5 = models.CharField(max_length=40)
    class6 = models.CharField(max_length=40)
    class7 = models.CharField(max_length=40)
    class8 = models.CharField(max_length=40, default='空闲')

    def __str__(self):
        return self.building + '-' + self.name


if __name__ == '__main__':
    Classroom.objects.filter(building='逸夫教学楼')
