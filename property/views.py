# property/views.py
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from rest_framework.permissions import AllowAny

from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated
from .serializers import PropertyUpdateSerializer ,PropertySerializer , PropertyCreateSerializer
from .models import Property
from django.shortcuts import get_object_or_404



class UpdatePropertyView(generics.UpdateAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertyUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return get_object_or_404(Property, pk=self.kwargs['pk'], landlord=self.request.user)
    
    
    

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        
        image_files = request.FILES.getlist('images')
        data = request.data.copy()
        
        if image_files:
            data['images'] = image_files

        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)
    
class GeocodeView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        query = request.query_params.get('q')
        if not query:
            return Response({"error": "Missing query parameter 'q'."}, status=status.HTTP_400_BAD_REQUEST)
        
        api_key = settings.OPENCAGE_API_KEY
        url = 'https://api.opencagedata.com/geocode/v1/json'
        params = {'q': query, 'key': api_key}

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return Response(response.json(), status=status.HTTP_200_OK)
        except requests.exceptions.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PropertyDeleteView(generics.DestroyAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Ensure that only the landlord who owns the property can delete it
        obj = get_object_or_404(Property, id=self.kwargs['id'], landlord=self.request.user)
        return obj
    
class PropertyCreateView(generics.CreateAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertyCreateSerializer

    def get_serializer_context(self):
        return {'request': self.request}