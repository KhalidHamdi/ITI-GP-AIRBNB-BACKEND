from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from rest_framework import status
from .models import *
from .serializers import *


@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
@permission_classes([])
def property_reservations(request, pk):
    try:
        property = get_object_or_404(Property, pk=pk)
        
        reservations = property.reservations.all()

        serializer = ReservationsListSerializer(reservations, many=True)

        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)

    except Property.DoesNotExist:
        return JsonResponse({'error': 'Property not found.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print("Error:", e)
        return JsonResponse({'error': 'An error occurred while retrieving reservations.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([AllowAny])
def book_property(request, pk):
    try:
        start_date = request.POST.get('start_date', '')
        end_date = request.POST.get('end_date', '')
        number_of_nights = request.POST.get('number_of_nights', '')
        total_price = request.POST.get('total_price', '')
        guests = request.POST.get('guests', '')

        property = Property.objects.get(pk=pk)

        Reservation.objects.create(
            property=property,
            start_date=start_date,
            end_date=end_date,
            number_of_nights=number_of_nights,
            total_price=total_price,
            guests=guests,
            created_by=request.user
            # created_by=None,           
        )
        return JsonResponse({'success': True})
    except Exception as e:
        print('Error from server: ', e)
        return JsonResponse({'success': False})
