# property/models.py

from django.db import models
import uuid
from django.conf import settings
from cloudinary.models import CloudinaryField
from useraccount.models import User
import logging
from .vector_db import add_data  # Import add_data from vector_db.py
from django.utils import timezone

logger = logging.getLogger(__name__)

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
    landlord = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    advertised_at = models.DateTimeField(null=True, blank=True)  # When the property was advertised
    is_advertised = models.BooleanField(default=False)
    paymob_order_id = models.CharField(max_length=255, blank=True, null=True)
    payment_status = models.CharField(max_length=20, blank=True, null=True)
    meta = models.TextField(blank=True, null=True)

    def image_url(self):
        # Assuming Cloudinary already gives you the full image URL
        return self.image.url if self.image else None

    def __str__(self):
        return f"{self.title} by {self.landlord.username}"

    def save(self, *args, **kwargs):
        # Automatically generate meta description
        self.meta = (
            f"{self.title} - A stunning property located in {self.city}, {self.country}. "
            f"This accommodation features {self.bedrooms} bedrooms and {self.bathrooms} bathrooms, "
            f"making it perfect for up to {self.guests} guests. "
            f"Enjoy your stay at just ${self.price_per_night} per night."
        )
        super().save(*args, **kwargs)
        
        # Try adding to vector database, log any errors without stopping save
        add_data(self.meta, self.id)



# this is for advertisment time out ...
    def start_advertisement(self):
        """Start advertising the property and record the current time."""
        self.is_advertised = True
        self.advertised_at = timezone.now()  # Set the current time when advertised
        self.save()

    def stop_advertisement(self):
        """Stop advertising the property."""
        self.is_advertised = False
        self.save()

    # Geocoding logic (commented out but included for completeness)
    # def save(self, *args, **kwargs):
    #     if not self.latitude or not self.longitude:
    #         geocoder = OpenCageGeocode(settings.OPENCAGE_API_KEY)
    #         query = f'{self.title}, {self.address}, {self.city}, {self.country}'
    #         results = geocoder.geocode(query)
    #         if results and len(results):
    #             self.latitude = results[0]['geometry']['lat']
    #             self.longitude = results[0]['geometry']['lng']
    #     super().save(args, **kwargs)

class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images')
    image = CloudinaryField('image', blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.property.title}"
