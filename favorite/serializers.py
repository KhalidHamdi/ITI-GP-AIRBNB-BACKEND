from rest_framework import serializers
from property.serializers import PropertiesListSerializer
from .models import Favorite

class FavoriteSerializer(serializers.ModelSerializer):
    property = PropertiesListSerializer(read_only=True)

    class Meta:
        model = Favorite
        fields = ('id', 'user', 'property', 'created_at')
