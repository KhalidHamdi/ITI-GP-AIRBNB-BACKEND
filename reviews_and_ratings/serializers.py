# reviews_and_ratings/serializers.py

from rest_framework import serializers
from .models import Review
from useraccount.models import User  # Adjust the import path if necessary

class UserSerializer(serializers.ModelSerializer):
    avatar_url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'avatar_url']

    def get_avatar_url(self, obj):
        if obj.avatar:
            return obj.avatar.url  
        return '/static/images/default-avatar.png' 

class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'comment', 'rating', 'cleanliness', 'accuracy', 'communication', 'location', 'check_in', 'value', 'user', 'created_at']

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value
