# property/api.py

from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from .serializers import (
    PropertiesListSerializer, 
    PropertiesDetailSerializer, 
    PropertyCreateSerializer, 
    PropertySerializer
)
from .models import Property, PropertyImage
from django.shortcuts import get_object_or_404
from .filter import PropertyFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from .vector_db import vector_db  # Import vector_db from vector_db.py
import logging

logger = logging.getLogger(__name__)

@api_view(['GET'])
@permission_classes([AllowAny])
def properties_list(request):
    logger.debug("Received properties_list request with parameters: %s", request.GET)

    try:
        properties = Property.objects.all()
        landlord_id = request.GET.get('landlord_id', '').strip()
        category = request.GET.get('category', '').strip()
        
        # Filter by landlord if provided
        if landlord_id:
            properties = properties.filter(landlord_id=landlord_id)
        
        # Filter by category if provided
        if category:
            properties = properties.filter(category=category)

        # Order by advertised first
        properties = properties.order_by('-is_advertised', 'id')
        
        filterset = PropertyFilter(request.GET, queryset=properties)
        
        if not filterset.is_valid():
            return Response({"error": "Invalid filters"}, status=status.HTTP_400_BAD_REQUEST)
        
        paginator = PageNumberPagination()
        paginator.page_size = 12  
        paginated_qs = paginator.paginate_queryset(filterset.qs, request)
        
        serializer = PropertiesListSerializer(paginated_qs, many=True)
        
        return paginator.get_paginated_response(serializer.data)

    except Exception as e:
        logger.error(f"Error in properties_list: {e}")
        return Response({'error': 'An error occurred while fetching properties.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_property(request):
    serializer = PropertyCreateSerializer(data=request.data, context={'request': request})

    if serializer.is_valid():
        try:
            property_instance = serializer.save()
            
            if 'images' in request.FILES:
                for image_file in request.FILES.getlist('images'):
                    PropertyImage.objects.create(property=property_instance, image=image_file)
            
            response_serializer = PropertiesDetailSerializer(property_instance, context={'request': request})
            return Response({'success': True, 'property': response_serializer.data}, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(f"Error in create_property: {e}")
            return Response({'error': 'An error occurred while creating the property.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([AllowAny])
def properties_detail(request, pk):
    try:
        property = get_object_or_404(Property, pk=pk)
        serializer = PropertiesDetailSerializer(property)
        return JsonResponse(serializer.data)
    except Exception as e:
        logger.error(f"Error in properties_detail: {e}")
        return JsonResponse({'error': 'Property not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([AllowAny])
def search_properties(request):
    try:
        city = request.GET.get('city', '').strip()
        country = request.GET.get('country', '').strip()
        guests = request.GET.get('guests', None)

        properties = Property.objects.all()

        if city:
            properties = properties.filter(city__icontains=city)

        if country:
            properties = properties.filter(country__icontains=country)

        if guests and guests.isdigit():
            properties = properties.filter(guests__gte=int(guests))

        serializer = PropertiesListSerializer(properties, many=True)
        return JsonResponse({'data': serializer.data})
    except Exception as e:
        logger.error(f"Error in search_properties: {e}")
        return JsonResponse({'error': 'An error occurred while searching properties.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([AllowAny])
def recommendation_search_properties(request):
    try:
        city = request.GET.get('city', '').strip().lower()  
        user_query = request.GET.get('query', '').strip().lower()  
        query = f"{city} {user_query}"

        if not vector_db:
            logger.error("vector_db is not initialized.")
            return JsonResponse({'error': 'Recommendation system is currently unavailable.'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        search_results = vector_db.similarity_search(query, k=5)  # Fetch top 5 results
        logger.debug(f"Search results: {search_results}")

        property_ids = [result.metadata.get('id') for result in search_results if 'id' in result.metadata]

        properties = Property.objects.filter(id__in=property_ids)
        
        if city:
            properties = properties.filter(city__icontains=city)

        serializer = PropertiesListSerializer(properties, many=True)
        return JsonResponse({'data': serializer.data})
    
    except Exception as e:
        logger.error(f"Error in recommendation_search_properties: {e}")
        return JsonResponse({'error': 'Could not perform recommendation search.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([AllowAny])
def search_suggestions(request):
    try:
        query = request.GET.get('query', '').strip()
        suggestions = Property.objects.filter(city__icontains=query).values_list('city', flat=True).distinct()
        suggestions_list = list(suggestions)
        return JsonResponse(suggestions_list[:5], safe=False)
    except Exception as e:
        logger.error(f"Error in search_suggestions: {e}")
        return JsonResponse({'error': 'Could not fetch suggestions.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
