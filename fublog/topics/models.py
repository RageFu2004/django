from django.db import models
from user.models import UserProfile

# Create your models here.

class Topic(models.Model):

    title = models.CharField(max_length=50, verbose_name='blog title')
    category = models.CharField(max_length=20, verbose_name='blog category')
    limit = models.CharField(max_length=20, verbose_name='blog limit')
    introduce = models.CharField(max_length=90, verbose_name='blog introduction')
    content = models.TextField(verbose_name='blog content')
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    objects = models.Manager()