from django.urls import path
from . import views
from . import api

urlpatterns = [
    path('paymob/', views.paymob, name='paymob'),
    path('initiate_payment/', views.initiate_payment, name='initiate_payment'),
    path('payment_callback/', views.payment_callback, name='payment_callback'), 
    path('callback_status/', views.callback_status, name='callback_status'),
    # path('api/post_state/', views.post_state, name='post_state'),
    

    path('reservation/<str:reservation_id>/update-details/', api.update_reservation_details, name='update-reservation-details'),
    path('reservation/<str:reservation_id>/initiate-payment/', api.initiate_payment, name='initiate-payment'),
    path('payment/webhook/', api.payment_status_webhook, name='payment-status-webhook'),
]
