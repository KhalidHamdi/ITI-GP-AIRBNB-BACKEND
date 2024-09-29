

from django.urls import path
from . import api
from uuid import UUID

urlpatterns = [
    path('', api.list_favorites, name='list_favorites'),
    path('add/<uuid:pk>/', api.add_favorite, name='add_favorite'),  
    path('remove/<uuid:pk>/', api.remove_favorite, name='remove_favorite'),
]
