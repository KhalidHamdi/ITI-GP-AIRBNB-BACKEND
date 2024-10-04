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


from langchain_openai import OpenAIEmbeddings
import chromadb
from langchain_community.vectorstores.chroma import Chroma
from langchain_core.documents import Document
import os



opena_api_key = os.getenv('opena_api_key')
embeddings = OpenAIEmbeddings(
    openai_api_key=opena_api_key, model="text-embedding-3-small")

vector_db = Chroma(
    collection_name="airbnb",
    embedding_function=embeddings,
    persist_directory="./chroma",
)


@api_view(['GET'])
@permission_classes([AllowAny])
def properties_list(request):
    print("Request Parameters: ", request.GET)

    properties = Property.objects.all()
    landlord_id = request.GET.get('landlord_id', '')
    category = request.GET.get('category', '')
    
    # Filter by landlord if provided
    if landlord_id:
        properties = properties.filter(landlord_id=landlord_id)
    
    # Filter by category if provided
    if category:
        properties = properties.filter(category__id=category)
    
    # Order by advertised first
    properties = properties.order_by('-is_advertised', 'id')
    
    # Apply any additional filters using the PropertyFilter class (if required)
    filterset = PropertyFilter(request.GET, queryset=properties)
    
    if not filterset.is_valid():
        return Response({"error": "Invalid filters"}, status=400)
    
    paginator = PageNumberPagination()
    paginator.page_size = 12  
    paginated_qs = paginator.paginate_queryset(filterset.qs, request)
    
    serializer = PropertiesListSerializer(paginated_qs, many=True)
    
    return paginator.get_paginated_response(serializer.data)



@api_view(['POST'])
@permission_classes([IsAuthenticated])  
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


@api_view(['GET'])
@permission_classes([AllowAny])
def recommendation_search_properties(request):
    query = request.GET.get('query', '').lower()  
    city = request.GET.get('city', '').lower()  

    search_results = vector_db.similarity_search(query, k=1)

    property_ids = []

    for result in search_results:
        if 'id' in result.metadata:
            property_ids.append(result.metadata['id'])

    if not property_ids:
        return JsonResponse({'data': []}, status=200)

    properties = Property.objects.filter(id__in=property_ids)
    if city:
        properties = properties.filter(city__icontains=city)

    serializer = PropertiesListSerializer(properties, many=True)
    return JsonResponse({'data': serializer.data})



@api_view(['GET'])
@permission_classes([AllowAny])
def search_suggestions(request):
    query = request.GET.get('query', '')
    suggestions = Property.objects.filter(city__icontains=query).values_list('city', flat=True).distinct()
    suggestions_list = list(suggestions)
    return JsonResponse(suggestions_list[:5],safe=False)
