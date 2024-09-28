from django.urls import path
from .views import GeocodeView

from . import api


urlpatterns = [
    path('', api.properties_list, name='api_properties_list'),
    path('create/', api.create_property, name='api_create_property'),
    path('<uuid:pk>/', api.properties_detail, name='api_properties_detail'),
    
    # URL Pattern for Geocode Endpoint :) 
    path('geocode/', GeocodeView.as_view(), name='geocode'),


]