from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework import status
from .models import *
from .serializers import *
from django.utils import timezone
from .models import Reservation
from datetime import timedelta


@api_view(['GET'])
@permission_classes([AllowAny])
def property_reservations(request, pk):
    try:
        reservations = Reservation.objects.filter(property_id=pk, is_paid=True)
        if not reservations.exists():
            return JsonResponse({'error': 'Property not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ReservationsListSerializer(reservations, many=True)
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)

    except Exception as e:
        print("Error:", e)
        return JsonResponse({'error': 'An error occurred while retrieving reservations.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([AllowAny])
def book_property(request, pk):
    try:
        data = request.data
        property = get_object_or_404(Property, pk=pk)

        reservation = Reservation.objects.create(
            property=property,
            start_date=data.get('start_date'),
            end_date=data.get('end_date'),
            number_of_nights=data.get('number_of_nights'),
            total_price=data.get('total_price'),
            guests=data.get('guests'),
            created_by=request.user
        )

        reservation_serializer = ReservationsListSerializer(reservation)
        return JsonResponse({'success': True, 'reservation': reservation_serializer.data}, status=status.HTTP_201_CREATED)

    except Exception as e:
        print('Error from server:', e)
        return JsonResponse({'success': False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def cancel_reservation(request, pk):
    try:
        reservation = Reservation.objects.get(id=pk, created_by=request.user)

        current_date = timezone.now().date()
        if reservation.start_date - current_date < timedelta(days=7):
            return JsonResponse(
                {'error': 'You can only cancel the reservation up to 7 days before the start date.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        reservation.delete()
        return JsonResponse({'message': 'Reservation cancelled successfully.'}, status=status.HTTP_200_OK)

    except Reservation.DoesNotExist:
        return JsonResponse({'error': 'Reservation not found.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print(f"Error from server: {e}")
        return JsonResponse({'error': 'An error occurred while cancelling the reservation.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
