from django.db import models
from person.models import Person


class PostCard(models.Model):
    name = models.CharField(max_length=20)
    url = models.CharField(max_length=50)
    content = models.TextField()

    def __str__(self):
        return self.name


class SendCard(models.Model):
    card = models.ForeignKey(PostCard, on_delete=models.CASCADE)
    from_person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="send")
    to_person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="receive")
    content = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    delete = models.BooleanField(default=False)

    def __str__(self):
        return self.from_person.name + '-' + self.to_person.name
