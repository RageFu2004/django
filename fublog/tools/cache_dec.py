from django.core.cache import cache
from .logging_dec import get_user_by_request


def cache_set(expire):
    def _cache_set(func):
        def wrapper(request, *args, **kwargs):

            if 't_id' in request.GET:
                return func(request, *args, **kwargs)
            visit_user = get_user_by_request(request)
            visitor_username = None
            if visit_user:
                visitor_username = visit_user.username
            author_username = kwargs['author_id']
            full_path = request.get_full_path()
            if visitor_username == author_username:
                cache_key = 'self_key_%s'%(full_path)
            else:
                cache_key = 'non_self_key%s'%(full_path)
            res = cache.get(cache_key)
            if res:
                return res
            res = func(request, *args, **kwargs)
            cache.set(cache_key, res, expire)
            return res
        return wrapper
    return _cache_set

