from django.db import models

# Create your models here.


class User(models.Model):
    username = models.CharField("Username", max_length=30, unique=True)
    password = models.CharField("pwd", max_length=32)
    created_time = models.DateTimeField("CreateTime", auto_now_add=True)
    updated_time = models.DateTimeField('UpdateTime', auto_now=True)
    email = models.EmailField(null=True)
    objects = models.Manager()

    def __str__(self):
        return "user_" + str(self.username)



