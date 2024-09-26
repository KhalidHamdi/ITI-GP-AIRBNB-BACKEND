from rest_framework import serializers
from .models import Review

class ReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = ['id', 'property', 'user', 'user_name', 'rating', 'comment', 'created_at']
        read_only_fields = ['user']

    def get_user_name(self, obj):
        return obj.user.name