from django.urls import path
from . import api

urlpatterns = [
    path('properties/<uuid:property_id>/reviews/', api.get_property_reviews, name='get_property_reviews'),
    path('properties/<uuid:property_id>/reviews/create/', api.create_review, name='create_review'),
]