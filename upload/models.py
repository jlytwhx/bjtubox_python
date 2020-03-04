from django.db import models
from user.models import User
import uuid


# Create your models here.
class File(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    upload_time = models.DateTimeField(auto_created=True)
