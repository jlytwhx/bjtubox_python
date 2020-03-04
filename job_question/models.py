from django.db import models


# Create your models here.
class Question(models.Model):
    openid = models.CharField(max_length=50)
    formId = models.CharField(max_length=50)
    name = models.CharField(max_length=30)
    user_type = models.CharField(max_length=10)
    question_type = models.CharField(max_length=10)
    phone = models.CharField(max_length=20)
    detail = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    # 企业
    company = models.CharField(max_length=80)

    # 学生
    student_id = models.CharField(max_length=15, null=True)
    student_graduate_year = models.IntegerField(null=True)

    # 回答
    answer = models.TextField(null=True)
    teacher = models.CharField(max_length=30, null=True)
