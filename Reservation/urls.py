from django.urls import path

from . import api
from .views import ReservationListView


urlpatterns = [
    path('<uuid:pk>/book/', api.book_property, name='api_book_property'),
    path('<uuid:pk>/reservations/', api.property_reservations, name='api_property_reservations'),
    path('properties/<uuid:property_id>/reservations/', ReservationListView.as_view(), name='reservation_list'),
    path('reservations/<uuid:pk>/cancel/', api.cancel_reservation, name='cancel_reservation'),


]