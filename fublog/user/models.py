from django.db import models

# Create your models here.


class UserProfile(models.Model):
    username = models.CharField(max_length=11, verbose_name="username", primary_key=True)
    nickname = models.CharField(max_length=30, verbose_name='nickname')
    password = models.CharField(max_length=32) # md5 encoding
    email = models.EmailField()
    phone = models.CharField(max_length=11)
    avatar = models.ImageField(upload_to='avatar', null=True)
    sign = models.CharField(max_length=50, verbose_name='personal signature', default='I Love UC Davis')
    info = models.CharField(max_length=150, verbose_name='personal introduction', default='')
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    class Meta:
        db_table = 'user_user_profile'
