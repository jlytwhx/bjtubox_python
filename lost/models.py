from django.db import models
from user.models import User
import uuid


class Lost(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    openid = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now=True)
    content = models.TextField()
    image = models.CharField(max_length=50, null=True, blank=True)
    type = models.SmallIntegerField(null=True, blank=True)
    at = models.CharField(max_length=20, null=True, blank=True)
    show = models.BooleanField(default=False)

    class Meta:
        ordering = ['-time']

    def __str__(self):
        return self.time.strftime(
            "%Y-%m-%d %H:%I:%S") + ' ' + self.openid.person.name + ' ' + self.content + ' ' + (
                   '已通过' if self.show else '未通过') + (
                   'https://mp.bjtu.edu.cn/file/user/image/{}"'.format(self.image) if self.image else '')


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    lost_id = models.ForeignKey(Lost, on_delete=models.CASCADE)
    openid = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now=True)
    content = models.TextField()
    image = models.CharField(max_length=50, null=True, blank=True)
    at = models.CharField(max_length=20, null=True, blank=True)
    show = models.BooleanField(default=False)

    class Meta:
        ordering = ['-time']

    def __str__(self):
        return self.time.strftime(
            "%Y-%m-%d %H:%I:%S") + ' ' + self.openid.person.name + ' ' + self.content + ' ' + (
                   '已通过' if self.show else '未通过')
