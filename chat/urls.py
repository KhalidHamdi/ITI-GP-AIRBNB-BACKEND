from django.urls import path
from . import api

urlpatterns = [
    path('',api.conversations_list, name='conversations_list')
]
