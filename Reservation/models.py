import uuid

from django.conf import settings
from django.db import models

from property.models import Property
from useraccount.models import User

class Reservation(models.Model):
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id=models.CharField(primary_key=True,default=uuid.uuid4, editable=False, max_length=36)

    property = models.ForeignKey(Property, related_name='reservations', on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    number_of_nights = models.IntegerField()
    guests = models.IntegerField()
    total_price = models.FloatField()
    created_by = models.ForeignKey(User, related_name='reservations', on_delete=models.CASCADE)
    # created_by = models.ForeignKey('useraccount.User', on_delete=models.CASCADE, related_name='reservations')

    created_at = models.DateTimeField(auto_now_add=True)
    
     
    # def __str__(self):
    #     return self.property
    