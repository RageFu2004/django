from django.urls import path
from . import views

urlpatterns = [
    path('visit', views.visitor_view),
    path('<str:author_id>', views.TopicViews.as_view())
]