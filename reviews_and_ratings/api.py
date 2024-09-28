from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from property.models import Property
from .models import Review
from .serializers import ReviewSerializer
from django.shortcuts import get_object_or_404



@api_view(['GET'])
@permission_classes([AllowAny])
def get_property_reviews(request, property_id):
    reviews = Review.objects.filter(property_id=property_id)
    serializer = ReviewSerializer(reviews, many=True)
    return Response(serializer.data)


from rest_framework.exceptions import ValidationError

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_review(request, property_id):
    user = request.user
    property = get_object_or_404(Property, id=property_id)
    
    # Check if the user has already reviewed the property
    existing_review = Review.objects.filter(property=property, user=user).first()

    if existing_review:
        raise ValidationError("You have already reviewed this property.")
    
    # Create a new review
    serializer = ReviewSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=user, property=property)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
