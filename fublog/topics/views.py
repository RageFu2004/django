from django.core.cache import cache
from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from tools.logging_dec import logging_check, get_user_by_request
from tools.cache_dec import cache_set
from .models import Topic
from user.models import UserProfile
from message.models import Message
import json

# Create your views here.
def make_visitor_res(author_topics):
    res = {'code': 200, 'data': {}}
    topics_res = []
    for topic in author_topics:
        d = {}
        d['id'] = topic.id
        d['title'] = topic.title
        d['category'] = topic.category
        d['created_time'] = topic.created_time.strftime("%Y-%m-%d %H:%M:%S")
        d['introduce'] = topic.introduce
        d['author'] = topic.author.username
        topics_res.append(d)
    res['data']['topics'] = topics_res
    res['data']['nickname'] = 'All writers'
    return res

def visitor_view(request):
    all_blogs = Topic.objects.filter(limit='public')
    res = make_visitor_res(all_blogs)
    return JsonResponse(res)






class TopicViews(View):

    def clear_topics_caches(self, request):
        path = request.path_info
        cache_key_p = ['topics_cache_self_', 'topics_cache_']
        cache_key_h = ['', '?category=Academic', '?category=Non-Academic']
        all_keys = []
        for key_p in cache_key_p:
            for key_h in cache_key_h:
                all_keys.append(key_p + path + key_h)
        cache.delete_many(all_keys)



    def make_topic_res(self, author, author_topic, is_self):
        # visit self
        if is_self:
            next_topic = Topic.objects.filter(id__gt=author_topic.id, author=author).first()
            last_topic = Topic.objects.filter(id__lt=author_topic.id, author=author).last()
        else:
            next_topic = Topic.objects.filter(id__gt=author_topic.id, author=author, limit='public').first()
            last_topic = Topic.objects.filter(id__lt=author_topic.id, author=author, limit='public').last()
        next_id = next_topic.id if next_topic else None
        next_title = next_topic.title if next_topic else ''
        last_id = last_topic.id if last_topic else None
        last_title = last_topic.title if last_topic else ''

        all_messages = Message.objects.filter(topic=author_topic).order_by('-created_time')

        msg_list = []
        rep_dic = {}
        m_count = 0
        for msg in all_messages:
            if msg.parent_message:
                rep_dic.setdefault(msg.parent_message, [])
                rep_dic[msg.parent_message].append({'msg_id': msg.id, 'publisher': msg.publisher.nickname,
                                                    'publisher_avatar': str(msg.publisher.avatar), 'content': msg.content,
                                                    'created_time': msg.created_time.strftime('%Y-%m-%d %H:%M:%S')})
            else:
                m_count += 1
                msg_list.append({'id': msg.id, 'content': msg.content, 'publisher': msg.publisher.nickname,
                                'publisher_avatar': str(msg.publisher.avatar),
                                 'created_time': msg.created_time.strftime('%Y-%m-%d %H:%M:%S'),
                                 'reply': []})
            for m in msg_list:
                if m['id'] in rep_dic:
                    m['reply'] = rep_dic[m['id']]
        res = {'code': 200, 'data': {}}
        res['data']['nickname'] = author.nickname
        res['data']['title'] = author_topic.title
        res['data']['category'] = author_topic.category
        res['data']['created_time'] = author_topic.created_time.strftime('%Y-%m-%d %H:%M:%S')
        res['data']['content'] = author_topic.content
        res['data']['introduce'] = author_topic.introduce
        res['data']['author'] = author.username
        res['data']['last_id'] = last_id
        res['data']['last_title'] = last_title
        res['data']['next_id'] = next_id
        res['data']['next_title'] = next_title
        res['data']['messages'] = msg_list
        res['data']['messages_count'] = m_count
        return res

    def make_topics_res(self, author, author_topics):
        res = {'code': 200, 'data': {}}
        topics_res = []
        for topic in author_topics:
            d = {}
            d['id'] = topic.id
            d['title'] = topic.title
            d['category'] = topic.category
            d['created_time'] = topic.created_time.strftime("%Y-%m-%d %H:%M:%S")
            d['introduce'] = topic.introduce
            d['author'] = author.nickname
            topics_res.append(d)
        res['data']['topics'] = topics_res
        res['data']['nickname'] = author.nickname
        return res



    @method_decorator(logging_check)
    def post(self, request, author_id):
        current_author = request.temp_user
        json_obj = request.body
        json_content = json.loads(json_obj)
        title = json_content['title']
        content = json_content['content']
        content_text = json_content['content_text']
        introduce = content_text[:30]
        limit = json_content['limit']
        category = json_content['category']
        if limit not in ['public', 'private']:
            result = {'code': 10300, 'error': 'limit option error'}
            return JsonResponse(result)

        Topic.objects.create(title=title, content=content, limit=limit,
                             category=category, introduce=introduce, author=current_author)
        self.clear_topics_caches(request)
        return JsonResponse({'code': 200})

    @method_decorator(cache_set(300))
    def get(self, request, author_id):
        try:
            author = UserProfile.objects.get(username=author_id)
        except Exception as e:
            result = {'code': 10301, 'error': 'The author does not exist'}
            return JsonResponse(result)

        visitor = get_user_by_request(request)
        visitor_username = None
        if visitor:
            visitor_username = visitor.username

        t_id = request.GET.get('t_id')
        if t_id:
            t_id = int(t_id)
            is_self = False
            if visitor_username == author_id:
                is_self = True
                try:
                    author_topic = Topic.objects.get(id=t_id, author_id=author_id)
                except Exception as e:
                    result = {'code': 10302, 'error': 'No Topic'}
                    return JsonResponse(result)
            else:

                try:
                    author_topic = Topic.objects.get(id=t_id, author_id=author_id, limit='public')
                except Exception as e:
                    result = {'code': 10303, 'error': 'No Topic'}
                    return JsonResponse(result)
            res = self.make_topic_res(author, author_topic, is_self)
            return JsonResponse(res)
        else:
            category = request.GET.get('category')
            if category in ['Academic', 'Non-Academic']:
                if visitor_username == author_id:
                    author_topics = Topic.objects.filter(author_id=author_id, category=category)
                else:
                    author_topics = Topic.objects.filter(author_id=author_id,
                                                         limit='public',
                                                         category=category)
            else:
                if visitor_username == author_id:
                    author_topics = Topic.objects.filter(author_id=author_id)
                else:
                    author_topics = Topic.objects.filter(author_id=author_id,
                                                         limit='public'
                                                         )

            res = self.make_topics_res(author, author_topics)
            return JsonResponse(res)



