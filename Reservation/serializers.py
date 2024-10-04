from django.db import models
from .models import *
from property.serializers import PropertiesListSerializer
from rest_framework import serializers

class ReservationsListSerializer(serializers.ModelSerializer):
    property = PropertiesListSerializer(read_only=True, many=False)
    
    class Meta:
        model = Reservation
        fields = (
            'id', 'start_date', 'end_date', 'number_of_nights', 'total_price', 'property', 'guests'
        )