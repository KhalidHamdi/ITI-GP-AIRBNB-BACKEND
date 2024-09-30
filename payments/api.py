from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .paymob import get_paymob_token, create_order, get_payment_key, card_payment
from Reservation.models import Reservation



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
def payment_status_webhook(request):
    try:
        paymob_order_id = request.data.get('order_id')
        payment_status = request.data.get('success')  # true/false from Paymob response

        reservation = Reservation.objects.get(paymob_order_id=paymob_order_id)

        if payment_status:  # If payment succeeded
            reservation.is_paid = True
            reservation.payment_status = 'Paid'
            reservation.save()
            return Response({'success': True, 'redirect_url': '/'})  # Redirect to home page

        else:  # If payment failed
            reservation.is_paid = False
            reservation.payment_status = 'Failed'
            reservation.save()
            return Response({'success': False, 'message': 'Payment failed.'}, status=400)

    except Reservation.DoesNotExist:
        return Response({'success': False, 'error': 'Reservation not found.'}, status=404)
    except Exception as e:
        return Response({'success': False, 'error': str(e)}, status=500)
