from django.conf import settings
from django.http import JsonResponse
import jwt

from user.models import UserProfile


def logging_check(func):
    def wrap(request, *args, **kwargs):
        token = request.META.get('HTTP_AUTHORIZATION')
        if not token:
            result = {'code': 403, 'error': 'Please login'}
            return JsonResponse(result)
        try:
            # caution: have to pass a algorithm parameter when using decode!
            res = jwt.decode(token, settings.JWT_TOKEN_KEY, algorithms="HS256")
        except Exception as e:
            result = {'code': 403, 'error': 'Please Login'}
            return JsonResponse(result)
        username = res['username']
        user = UserProfile.objects.get(username=username)
        request.temp_user = user
        return func(request, *args, **kwargs)
    return wrap

def get_user_by_request(request):
    token = request.META.get('HTTP_AUTHORIZATION')
    if not token:
        return None
    try:
        res = jwt.decode(token, settings.JWT_TOKEN_KEY, algorithms='HS256')
    except Exception as e:
        return None

    username = res['username']
    user = UserProfile.objects.get(username=username)
    return user
