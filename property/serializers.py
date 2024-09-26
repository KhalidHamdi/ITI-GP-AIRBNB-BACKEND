from .models import Property
from rest_framework import serializers
from django.db.models import Avg

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

    class Meta:
        model = Property
        fields = (
            'id',
            'title',
            'description',
            'price_per_night',
            'image_url',
            'bedrooms',
            'bathrooms',
            'guests',
            'country',
            'category',
            'average_rating',
            'reviews_count',
            'landlord',
        )

    def get_image_url(self, obj):
        return obj.image.url

    def get_average_rating(self, obj):
        return obj.reviews.aggregate(Avg('rating'))['rating__avg']

    def get_reviews_count(self, obj):
        return obj.reviews.count()