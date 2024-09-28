from .models import Property
from rest_framework import serializers
from django.db.models import Avg
from useraccount.serializers import UserDetailSerializer


class PropertiesListSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    reviews_count = serializers.SerializerMethodField()

    class Meta:
        model = Property
        fields = (
            'id',
            'title',
            'price_per_night',
            'image_url',
            'average_rating',
            'reviews_count',
        )

    def get_image_url(self, obj):
        return obj.image.url

    def get_average_rating(self, obj):
        return obj.reviews.aggregate(Avg('rating'))['rating__avg']

    def get_reviews_count(self, obj):
        return obj.reviews.count()

class PropertiesDetailSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    reviews_count = serializers.SerializerMethodField()
    latitude = serializers.ReadOnlyField()
    longitude = serializers.ReadOnlyField()
    landlord = UserDetailSerializer(read_only=True, many=False)

    class Meta:
        model = Property
        fields = (
            'id', 'title', 'description', 'price_per_night', 'image_url',
            'bedrooms', 'bathrooms', 'guests', 'city', 'address',
            'country', 'category', 'latitude', 'longitude', 
            'average_rating', 'reviews_count','landlord',
        )

    def get_image_url(self, obj):
        return obj.image.url

    def get_average_rating(self, obj):
        return obj.reviews.aggregate(Avg('rating'))['rating__avg']

    def get_reviews_count(self, obj):
        return obj.reviews.count()
    
    
class PropertyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = (
            'title',
            'description',
            'price_per_night',
            'bedrooms',
            'bathrooms',
            'guests',
            'country',
            'country_code',
            'category',
            'image',  
            'city',
            'address',
        )
        
    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['landlord'] = request.user  # Assign the logged-in user as the landlord
        return super().create(validated_data)