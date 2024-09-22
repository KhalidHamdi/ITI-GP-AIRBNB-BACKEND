from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.shortcuts import get_object_or_404
from rest_framework import status
from .models import *
from .serializers import *
@api_view(['GET'])
def property_reservations(request, pk):
    try:
        # Get property or 404
        property = get_object_or_404(Property, pk=pk)
        
        # Get all reservations for the property
        reservations = property.reservations.all()

        # Serialize data
        serializer = ReservationsListSerializer(reservations, many=True)

        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)

    except Property.DoesNotExist:
        return JsonResponse({'error': 'Property not found.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print("Error:", e)
        return JsonResponse({'error': 'An error occurred while retrieving reservations.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def property_reservations(request, pk):
    property = Property.objects.get(pk=pk)
    reservations = property.reservations.all()

    serializer = ReservationsListSerializer(reservations, many=True)

    return JsonResponse(serializer.data, safe=False)
