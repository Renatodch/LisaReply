from django.shortcuts import redirect
from django.urls import path, re_path

from app.chat import Chatbot

from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('tutorial/', views.tutorial, name='tutorial'),
    path('delete/', views.delete, name='delete'),
    path('message/', views.message, name='message'),
    re_path(r'^.*$', lambda request: redirect('home')),
]
