import uuid

from django.conf import settings
from django.db import models

from property.models import Property
from useraccount.models import User

class Reservation(models.Model):
    property = models.ForeignKey(Property, related_name='reservations', on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    number_of_nights = models.IntegerField()
    guests = models.IntegerField()
    total_price = models.FloatField()
    created_by = models.ForeignKey(User, related_name='reservations', on_delete=models.CASCADE)
    # created_by = models.ForeignKey(User, related_name='reservations', on_delete=models.CASCADE, null=True)
    # created_by = models.ForeignKey('useraccount.User', on_delete=models.CASCADE, related_name='reservations')

    created_at = models.DateTimeField(auto_now_add=True)

    id=models.CharField(primary_key=True,default=uuid.uuid4, editable=False, max_length=36)
    
    
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    
    
    paymob_order_id = models.CharField(max_length=100, blank=True, null=True)
    is_paid = models.BooleanField(default=False)
    payment_status = models.CharField(max_length=50, blank=True, null=True)
    
    
     
    def __str__(self):
        return f"Reservation for {self.property.title}"
    
    def cancel_reservation(self):
        """Cancels the reservation if it is valid to do so (before 7 days)."""
        current_date = timezone.now().date()
        days_until_start = (self.start_date - current_date).days

        if days_until_start < 7:
            raise ValidationError("You can only cancel the reservation up to 7 days before the start date.")
        
        self.delete()  
