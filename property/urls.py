from django.urls import path

from . import api


urlpatterns = [
    path('', api.properties_list, name='api_properties_list'),
    path('create/', api.create_property, name='api_create_property'),
    path('<uuid:pk>/', api.properties_detail, name='api_properties_detail'),
    path('search/',api.search_properties,name='search_properties'),
    path('search_suggestions/',api.search_suggestions, name='search_suggestions'),
]