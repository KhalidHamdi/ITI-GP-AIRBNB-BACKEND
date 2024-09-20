from .models import Property
from rest_framework import serializers 

class PropertiesListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Property
        fields = (
            'id',
            'title',
            'price_per_night',
            'image_url',
        )

