from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from .models import UserProfile
import json
from django.http import JsonResponse
import hashlib
from tools.logging_dec import logging_check
# Create your views here.


@logging_check
def users_views(request, username):
    if request.method != 'POST':
        result = {'code': 10104, 'error': 'The username is error'}
        return JsonResponse(result)
    # use the user from decorator
    user = request.temp_user

    avatar = request.FILES['avatar']
    user.avatar = avatar
    user.save()
    return JsonResponse({'code': 200})


class UserViews(View):
    # all get method goes into this function
    def get(self, request, username=None):
        if username:
            try:
                user = UserProfile.objects.get(username=username)
            except Exception as e:
                result = {'code': 10102, 'error': 'Invalid username'}
                return JsonResponse(result)
            result = {'code': 200, 'username': username, 'data': {'info': user.info,
                                                                  'sign': user.sign,
                                                                  'nickname': user.nickname,
                                                                  'avatar': str(user.avatar)}}
            return JsonResponse(result)

        else:
            pass

    # all post method goes into this function
    def post(self, request):
        json_str = request.body
        json_obj = json.loads(json_str)
        username = json_obj['username']
        email = json_obj['email']
        password_1 = json_obj['password_1']
        password_2 = json_obj['password_2']
        users = UserProfile.objects.all()
        not_reg = True
        for user in users:
            if user.username == username:
                not_reg = False
                break
        if not_reg:
            if '@ucdavis.edu' in email:
                if password_1 == password_2:
                    coded_password = hashlib.md5()
                    coded_password.update(password_1.encode())
                    new_user = UserProfile.objects.create(username=username, nickname=username, email=email,
                                                          password=coded_password.hexdigest())
                    result = {'code': 200, 'username': username, 'data': {}}
                    return JsonResponse(result)
                else:
                    result = {'code': 10003, 'error': 'Your passwords are not the same'}
                    return JsonResponse(result)

            else:
                result = {'code': 10002, 'error': 'You must enter your ucdavis email(end with @ucdavis.edu)'}
                return JsonResponse(result)
        else:
            result = {'code': 10001, 'error': 'Invalid username: already registered'}
            return JsonResponse(result)

    @method_decorator(logging_check)
    def put(self, request, username):
        json_body = request.body
        content = json.loads(json_body)
        nickname = content['nickname']
        sign = content['sign']
        info = content['info']

        if username:
            user = request.temp_user
            user.sign = sign
            user.nickname = nickname
            user.info = info
            user.save()
            return JsonResponse({'code': 200})
        else:
            result = {'code': 10201, 'error': 'Your username does not exist'}
            return JsonResponse(result)



