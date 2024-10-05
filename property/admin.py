# property/admin.py

from django.contrib import admin
from .models import Property, PropertyImage

# admin.site.register(Property)
# admin.site.register(PropertyImage)

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'landlord', 'is_advertised', 'price_per_night')
    search_fields = ('title', 'description', 'city', 'country')
    list_filter = ('is_advertised', 'category', 'country')

@admin.register(PropertyImage)
class PropertyImageAdmin(admin.ModelAdmin):
    list_display = ('property', 'image', 'uploaded_at')
    search_fields = ('property__title',)
    list_filter = ('uploaded_at',)
