import time

import jwt
from django.http import JsonResponse
from django.shortcuts import render
from user.models import UserProfile
import json
import hashlib
from django.conf import settings
# Create your views here.
# only post request possible so fbv


def tokens(request):
    if request.method == 'POST':
        js_body = request.body
        js_obj = json.loads(js_body)
        username = js_obj['username']
        password = js_obj['password']
        all_users = UserProfile.objects.all()
        user_now = None
        for user in all_users:
            if user.username == username:
                user_now = user
                break
        if user_now:
            hash_code = hashlib.md5()
            hash_code.update(password.encode())
            #print(hash_code.hexdigest())
            if user_now.password == hash_code.hexdigest():
                token = make_token(username)
                result = {'code': 200, 'username': username, 'data': {'token': token}}
                return JsonResponse(result)
            else:
                result = {'code': 10011, 'error': 'Your Username or Password is wrong'}
                return JsonResponse(result)
        else:
            result = {'code': 10011, 'error': 'Your Username or Password is wrong'}
            return JsonResponse(result)
    else:
        result = {'code': 10010, 'error': 'Forbidden: You are not using POST'}
        return JsonResponse(result)


def make_token(username, expire=3600*24):
    key = settings.JWT_TOKEN_KEY
    now_time = time.time()
    payload_data = {'username': username, 'exp': now_time+expire}
    return jwt.encode(payload_data, key, algorithm='HS256')
