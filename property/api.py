from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import status
from .serializers import PropertiesListSerializer, PropertiesDetailSerializer, PropertyCreateSerializer
from .models import Property
from django.shortcuts import get_object_or_404
from .filter import PropertyFilter ;
from rest_framework.permissions import IsAuthenticated

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

@api_view(['GET'])
@permission_classes([AllowAny])
def properties_list(request):
    print("Request Parameters: ", request.GET)

    filterset = PropertyFilter(request.GET, queryset=Property.objects.all())

    if not filterset.is_valid():
        return Response({"error": "Invalid filters"}, status=400)

    paginator = PageNumberPagination()
    paginator.page_size = 12  # Properties per page
    paginated_qs = paginator.paginate_queryset(filterset.qs, request)

    serializer = PropertiesListSerializer(paginated_qs, many=True)
    
    return paginator.get_paginated_response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])  # Ensure only authenticated users can access this endpoint
def create_property(request):
    serializer = PropertyCreateSerializer(data=request.data, context={'request': request})

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


@api_view(['GET'])
@permission_classes([AllowAny])
def search_properties(request):
    city=request.GET.get('city','')
    country=request.GET.get('country','')
    guests=request.GET.get('guests')

    properties=Property.objects.all()

    if city:
        properties=properties.filter(city__icontains=city)
    if  country:
        properties=properties.filter(country__icontains=country)
    if  guests:
        properties=properties.filter(guests__gte=guests)
    
    serializer=PropertiesListSerializer(properties,many=True)
    return  JsonResponse({'data':serializer.data})

@api_view(['GET'])
@permission_classes([AllowAny])
def search_suggestions(request):
    query = request.GET.get('query', '')
    suggestions = Property.objects.filter(city__icontains=query).values_list('city', flat=True).distinct()
    suggestions_list = list(suggestions)
    return JsonResponse(suggestions_list[:5],safe=False)
