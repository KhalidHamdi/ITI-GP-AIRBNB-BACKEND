
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from .paymob import get_paymob_token, create_order, get_payment_key, card_payment
from Reservation.models import Reservation
from property.models import Property
from django.shortcuts import redirect
from django.http import HttpResponseRedirect



@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def update_reservation_details(request, reservation_id):
    try:
        reservation = Reservation.objects.get(id=reservation_id, created_by=request.user)

        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        email = request.data.get('email')
        phone = request.data.get('phone')

        reservation.first_name = first_name
        reservation.last_name = last_name
        reservation.email = email
        reservation.phone = phone
        reservation.save()

        return Response({'success': True, 'message': 'Reservation details updated successfully.'})

    except Reservation.DoesNotExist:
        return Response({'success': False, 'error': 'Reservation not found.'}, status=404)
    except Exception as e:
        return Response({'success': False, 'error': str(e)}, status=500)


@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def initiate_payment(request, reservation_id):
    try:
        reservation = Reservation.objects.get(id=reservation_id, created_by=request.user)
        
        paymob_token = get_paymob_token()

        amount_cents = int(reservation.total_price * 100)
        order_id = create_order(paymob_token, amount_cents)

        payment_token = get_payment_key(paymob_token, order_id, amount_cents)

        reservation.paymob_order_id = order_id
        reservation.save()

        iframe_url = card_payment(payment_token)

        return Response({'success': True, 'iframe_url': iframe_url})

    except Reservation.DoesNotExist:
        return Response({'success': False, 'error': 'Reservation not found.'}, status=404)
    except Exception as e:
        return Response({'success': False, 'error': str(e)}, status=500)

@api_view(['POST'])
def initiate_property_ad_payment(request, property_id):
    try:
        property = Property.objects.get(id=property_id, landlord=request.user)

        advertisement_cost = request.data.get('cost', 0) 
        
        paymob_token = get_paymob_token()
        amount_cents = int(advertisement_cost) * 100  
        order_id = create_order(paymob_token, amount_cents)

        payment_token = get_payment_key(paymob_token, order_id, amount_cents)

        property.paymob_order_id = order_id
        property.save()

        iframe_url = card_payment(payment_token)

        return Response({'success': True, 'iframe_url': iframe_url})

    except Property.DoesNotExist:
        return Response({'success': False, 'error': 'Property not found.'}, status=404)
    except Exception as e:
        return Response({'success': False, 'error': str(e)}, status=500)


@csrf_exempt
@api_view(['POST', 'GET'])
@permission_classes([AllowAny])
def payment_status_webhook(request):
    print("Hellllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllo")
    transaction_id = request.GET.get('id')
    payment_status_str = request.GET.get('success')
    paymob_order_id = request.GET.get('order')
    payment_status = True if payment_status_str == 'true' else False
    
    # Check if this is for a Reservation or Property
    try:
        reservation = Reservation.objects.get(paymob_order_id=paymob_order_id)
        reservation.is_paid = payment_status
        reservation.payment_status = 'Paid' if payment_status else 'Failed'
        reservation.save()
    except Reservation.DoesNotExist:
        property = Property.objects.get(paymob_order_id=paymob_order_id)
        property.is_advertised = payment_status
        property.payment_status = 'Paid' if payment_status else 'Failed'
        property.save()
    
    if payment_status: 
        print(f"Transaction {transaction_id} for Order {paymob_order_id} successfully processed.")

    return Response({'success': True})

@api_view(['GET'])
@permission_classes([AllowAny])
def payment_redirect(request):
    success = request.query_params.get('success')
    payment_status_str = request.GET.get('success')
    print ("Payment status ...........................", payment_status_str)
    transaction_id = request.GET.get('id')
    print ("Payment id ...........................", transaction_id)
    paymob_order_id  = request.GET.get('order')
    print ("Payment order id ...........................", paymob_order_id)
    payment_status = True if payment_status_str == 'true' else False
    
    try:
        reservation = Reservation.objects.get(paymob_order_id=paymob_order_id)
        reservation.is_paid = payment_status
        reservation.payment_status = 'Paid' if payment_status else 'Failed'
        reservation.save()
    except Reservation.DoesNotExist:
        property = Property.objects.get(paymob_order_id=paymob_order_id)
        property.is_advertised = payment_status
        property.payment_status = 'Paid' if payment_status else 'Failed'
        property.save()
    
    if success == 'true':
        # return HttpResponseRedirect("http://localhost:5173/?message=Payment successful")
        return HttpResponseRedirect("https://airiti.netlify.app/?message=Payment successful")
    else:
        # return HttpResponseRedirect("http://localhost:5173/?message=Payment failed")
        return HttpResponseRedirect("https://airiti.netlify.app/?message=Payment failed")