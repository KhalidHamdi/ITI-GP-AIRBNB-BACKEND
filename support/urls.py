from django.urls import path
from . import api

urlpatterns = [
    path('api/contact-support/', api.contact_support, name='contact-support'),
]
