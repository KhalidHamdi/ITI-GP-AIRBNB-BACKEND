from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid
from property.models import Property
from useraccount.models import User

class Review(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    cleanliness = models.DecimalField(max_digits=2, decimal_places=1, validators=[MinValueValidator(1.0), MaxValueValidator(5.0)])
    accuracy = models.DecimalField(max_digits=2, decimal_places=1, validators=[MinValueValidator(1.0), MaxValueValidator(5.0)])
    communication = models.DecimalField(max_digits=2, decimal_places=1, validators=[MinValueValidator(1.0), MaxValueValidator(5.0)])
    location = models.DecimalField(max_digits=2, decimal_places=1, validators=[MinValueValidator(1.0), MaxValueValidator(5.0)])
    check_in = models.DecimalField(max_digits=2, decimal_places=1, validators=[MinValueValidator(1.0), MaxValueValidator(5.0)])
    value = models.DecimalField(max_digits=2, decimal_places=1, validators=[MinValueValidator(1.0), MaxValueValidator(5.0)])
    
    rating = models.DecimalField(max_digits=2, decimal_places=1, validators=[MinValueValidator(1.0), MaxValueValidator(5.0)], blank=True, null=True)
    
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('property', 'user')

    def __str__(self):
        return self.comment
