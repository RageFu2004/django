from django.http import JsonResponse
from django.shortcuts import render
from tools.logging_dec import logging_check
import json
from message.models import Message

from topics.models import Topic


# Create your views here.

@logging_check
def message_view(request, topic_id):
    user = request.temp_user
    json_str = request.body
    json_obj = json.loads(json_str)
    content = json_obj['content']
    parent_id = json_obj.get('parent_id', 0)
    try:
        topic = Topic.objects.get(id=topic_id)
    except Exception as e:
        result = {'code': 10400, 'error': 'The topic does not exist'}
        return JsonResponse(result)
    Message.objects.create(topic=topic, content=content, parent_message=parent_id, publisher=user)
    return JsonResponse({'code': 200})

