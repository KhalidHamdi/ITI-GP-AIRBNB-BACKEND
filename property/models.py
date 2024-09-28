from django.db import models
import uuid
from django.conf import settings
from cloudinary.models import CloudinaryField
from opencage.geocoder import OpenCageGeocode
from useraccount.models import User


class Property(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    price_per_night = models.IntegerField()
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField()
    guests = models.IntegerField()
    city = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255)
    country_code = models.CharField(max_length=10)
    category = models.CharField(max_length=255)
    image = CloudinaryField('image', blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    landlord = models.ForeignKey(User, related_name='properties', on_delete=models.CASCADE ,null = False)

    
    def image_url(self):
        return f'{settings.WEBSITE_URL}{self.image.url}'

    def __str__(self):
        return (self.title)

    def save(self, *args, **kwargs):
        if not self.latitude or not self.longitude:
            geocoder = OpenCageGeocode(settings.OPENCAGE_API_KEY)
            query = f'{self.title}, {self.address}, {self.city}, {self.country}'
            results = geocoder.geocode(query)
            if results and len(results):
                self.latitude = results[0]['geometry']['lat']
                self.longitude = results[0]['geometry']['lng']
        super().save(*args, **kwargs)