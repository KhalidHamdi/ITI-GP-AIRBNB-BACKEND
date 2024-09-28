# Reservation/views.py
from rest_framework import generics, permissions
from .models import Reservation
from .serializers import ReservationSerializer
from property.models import Property
from django.shortcuts import get_object_or_404

class ReservationListView(generics.ListAPIView):
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        property_id = self.kwargs.get('property_id')
        property_obj = get_object_or_404(Property, id=property_id)
        return Reservation.objects.filter(property=property_obj)
