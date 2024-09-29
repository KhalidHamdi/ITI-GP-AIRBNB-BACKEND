from django.urls import path
from . import api

urlpatterns = [
    path('favorites/', api.list_favorites, name='list_favorites'),
    path('favorites/add/<int:pk>/', api.add_favorite, name='add_favorite'),
    path('favorites/remove/<int:pk>/', api.remove_favorite, name='remove_favorite'),
]
