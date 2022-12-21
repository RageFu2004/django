from django.db import models
from user.models import User
# Create your models here.


class Note(models.Model):
    title = models.CharField("Title", max_length=100)
    content = models.TextField("Contents")
    created_time = models.DateTimeField("CreateTime", auto_now_add=True)
    updated_time = models.DateTimeField("UpdateTime", auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    objects = models.Manager()