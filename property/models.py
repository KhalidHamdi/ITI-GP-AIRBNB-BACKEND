
from django.db import models
import uuid
from django.conf import settings
from cloudinary.models import CloudinaryField
from opencage.geocoder import OpenCageGeocode
from useraccount.models import User
from langchain_openai import OpenAIEmbeddings
import chromadb
from langchain_community.vectorstores.chroma import Chroma
from langchain_core.documents import Document
import os


opena_api_key = os.getenv('opena_api_key')
embeddings = OpenAIEmbeddings(
    openai_api_key=opena_api_key, model="text-embedding-3-small")

vector_db = Chroma(
    collection_name="airbnb",
    embedding_function=embeddings,
    persist_directory="./chroma",
)

def add_data(vector_db, meta_data, id):
    doc = Document(
        page_content=meta_data,
        metadata={"id": str(id)}  
    )
    vector_db.add_documents(
        documents=[doc]
    )






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
    landlord = models.ForeignKey(User, on_delete=models.CASCADE, null=False,)
    is_advertised = models.BooleanField(default=False)
    paymob_order_id = models.CharField(max_length=255, blank=True, null=True) 
    payment_status = models.CharField(max_length=20, blank=True, null=True)
    meta = models.TextField(blank=True, null=True)



    def image_url(self):
        return f'{settings.WEBSITE_URL}{self.image.url}'

    def str(self):
        return (self.title)
    
    def __str__(self):
        return f"Property {self.title} by {self.landlord}"
    
    def save(self, *args, **kwargs):
        self.meta = (
        f"{self.title} - A stunning property located in {self.city}, {self.country}. "
        f"This accommodation features {self.bedrooms} bedrooms and {self.bathrooms} bathrooms, "
        f"making it perfect for up to {self.guests} guests. "
        f"Enjoy your stay at just ${self.price_per_night} per night."
        )
        super().save(*args, **kwargs)
        add_data(vector_db, self.meta, self.id)



    # def save(self, args, **kwargs):
    #     if not self.latitude or not self.longitude:
    #         geocoder = OpenCageGeocode(settings.OPENCAGE_API_KEY)
    #         query = f'{self.title}, {self.address}, {self.city}, {self.country}'
    #         results = geocoder.geocode(query)
    #         if results and len(results):
    #             self.latitude = results[0]['geometry']['lat']
    #             self.longitude = results[0]['geometry']['lng']
    #     super().save(args, **kwargs)