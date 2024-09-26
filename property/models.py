from django.db import models
import uuid
from django.conf import settings 
from cloudinary.models import CloudinaryField
from useraccount.models import User


class Property(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    price_per_night = models.IntegerField()
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField()
    guests = models.IntegerField()
    country = models.CharField(max_length=255)
    country_code = models.CharField(max_length=10)
    category = models.CharField(max_length=255)
    image = CloudinaryField('image', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    landlord = models.ForeignKey(User, related_name='properties', on_delete=models.CASCADE)
    
    def image_url(self):
        return f'{settings.WEBSITE_URL}{self.image.url}'
    def __str__(self):
        return self.title