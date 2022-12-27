from django.db import models

from topics.models import Topic

from user.models import UserProfile


# Create your models here.

class Message(models.Model):
    content = models.CharField(max_length=50)
    created_time = models.DateTimeField(auto_now_add=True)
    parent_message = models.IntegerField(verbose_name='comment_id')
    publisher = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    objects = models.Manager()