from django.urls import path
from .views import PropertyDeleteView, UpdatePropertyView , GeocodeView

from . import api


urlpatterns = [
    path('', api.properties_list, name='api_properties_list'),
    path('create/', api.create_property, name='api_create_property'),
    path('<uuid:pk>/', api.properties_detail, name='api_properties_detail'),
    path('search/',api.search_properties,name='search_properties'),
    path('search_suggestions/',api.search_suggestions, name='search_suggestions'),    
    # URL Pattern for Geocode Endpoint :) 
    path('geocode/', GeocodeView.as_view(), name='geocode'),
    path('<uuid:pk>/update/', UpdatePropertyView.as_view(), name='api_update_property'),  # for the updating
    path('properties/<uuid:id>/delete/', PropertyDeleteView.as_view(), name='property-delete'),




]