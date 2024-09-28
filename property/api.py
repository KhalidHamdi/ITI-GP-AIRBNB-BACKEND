from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import status
from .serializers import PropertiesListSerializer, PropertiesDetailSerializer, PropertyCreateSerializer
from .models import Property
from django.shortcuts import get_object_or_404
from .filter import PropertyFilter ;

@api_view(['GET'])
@permission_classes([AllowAny])
def properties_list(request):
    # Log request parameters to ensure they are received correctly
    print("Request Parameters: ", request.GET)
    
    # Apply filter based on the request parameters
    filterset = PropertyFilter(request.GET, queryset=Property.objects.all())
    
    # Check if the filterset is valid
    if not filterset.is_valid():
        # Log errors for debugging
        print("Filter Errors: ", filterset.errors)

    # Use the filtered queryset for serialization
    serializer = PropertiesListSerializer(filterset.qs, many=True)
    
    return JsonResponse({
        'data': serializer.data
    })


@api_view(['POST'])
@permission_classes([AllowAny])  
def create_property(request):
    serializer = PropertyCreateSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save() 
        return JsonResponse({'success': True, 'property': serializer.data}, status=status.HTTP_201_CREATED)
    else:
        return JsonResponse({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([AllowAny])
def properties_detail(request, pk):
    property = get_object_or_404(Property, pk=pk)
    serializer = PropertiesDetailSerializer(property)
    return JsonResponse(serializer.data)
