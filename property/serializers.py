
from .models import Property, PropertyImage
from rest_framework import serializers
from django.db.models import Avg
from useraccount.serializers import UserDetailSerializer
from favorite.models import Favorite
from Reservation.models import Reservation

class PropertyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyImage
        fields = ['image']

    def to_representation(self, instance):
        return {'image': instance.image.url if instance.image else None}

class PropertiesListSerializer(serializers.ModelSerializer):
    images = PropertyImageSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()
    reviews_count = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()

    class Meta:
        model = Property
        fields = (
            'id',
            'title',
            'price_per_night',
            'images',
            'average_rating',
            'reviews_count',
            'is_favorited',
            'landlord',
            'is_advertised',
        )

    def get_average_rating(self, obj):
        return obj.reviews.aggregate(Avg('rating'))['rating__avg']

    def get_reviews_count(self, obj):
        return obj.reviews.count()
    
    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Favorite.objects.filter(user=request.user, property=obj).exists()
        return False

class PropertiesDetailSerializer(serializers.ModelSerializer):
    images = PropertyImageSerializer(many=True, read_only=True)  
    average_rating = serializers.SerializerMethodField()
    reviews_count = serializers.SerializerMethodField()
    latitude = serializers.ReadOnlyField()
    longitude = serializers.ReadOnlyField()
    landlord = UserDetailSerializer(read_only=True, many=False)
    is_favorited = serializers.SerializerMethodField()
    is_advertised =  serializers.ReadOnlyField()

    class Meta:
        model = Property
        fields = (
            'id', 'title', 'description', 'price_per_night', 'images',
            'bedrooms', 'bathrooms', 'guests', 'city', 'address',
            'country', 'category', 'latitude', 'longitude', 
            'average_rating', 'reviews_count','landlord', 'is_favorited' , 'is_advertised' ,
        )

    def get_average_rating(self, obj):
        return obj.reviews.aggregate(Avg('rating'))['rating__avg']

    def get_reviews_count(self, obj):
        return obj.reviews.count()
    
    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Favorite.objects.filter(user=request.user, property=obj).exists()
        return False

class PropertyCreateSerializer(serializers.ModelSerializer):
    images = PropertyImageSerializer(many=True, required=False)

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
            'city',
            'address',
            'images',
        )

    def create(self, validated_data):
        images_data = validated_data.pop('images', [])
        request = self.context.get('request')
        landlord = request.user 

        property_instance = Property.objects.create(landlord=landlord, **validated_data)

        # Handle images
        for image_data in images_data:
            PropertyImage.objects.create(property=property_instance, **image_data)

        return property_instance

class PropertyUpdateSerializer(serializers.ModelSerializer):
    images = PropertyImageSerializer(many=True, required=False)  

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
            'city',
            'address',
            'images',
        )

    def update(self, instance, validated_data):
        images_data = validated_data.pop('images', [])
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()

        # Update images
        if images_data:
            instance.images.all().delete()  
            for image_data in images_data:
                PropertyImage.objects.create(property=instance, **image_data)

        return instance

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'

class PropertySerializer(serializers.ModelSerializer):
    bookings = BookingSerializer(many=True, read_only=True)
    images = PropertyImageSerializer(many=True, read_only=True)

    class Meta:
        model = Property
        fields = ['category', 'title', 'description', 'price_per_night', 'bedrooms', 'bathrooms', 'guests', 'country', 'country_code', 'city', 'address', 'images']

    def get_images(self, obj):
        return [cloudinary_url(image.image.public_id)[0] for image in obj.images.all()]