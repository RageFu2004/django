from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('edit', views.note_edit),
    path('present', views.note_present),
    path('create', views.note_create),
    path('edit', views.note_edit)
]