from django.urls import path
from . import views
from . import api

urlpatterns = [
    path('reservation/<str:reservation_id>/update-details/', api.update_reservation_details, name='update-reservation-details'),
    path('reservation/<str:reservation_id>/initiate-payment/', api.initiate_payment, name='initiate-payment'),
    path('property-ad/<str:property_id>/initiate-payment/', api.initiate_property_ad_payment, name='initiate-property-ad-payment'),
    # path('property-ad/status-webhook/', api.payment_status_webhook, name='property-ad-payment-status-webhook'),
    # path('property-ad/redirect/', api.payment_redirect, name='property-ad-redirect'),
    path('status-webhook/', api.payment_status_webhook, name='payment-status-webhook'),
    path('redirect/', api.payment_redirect, name='redirect'),
]
