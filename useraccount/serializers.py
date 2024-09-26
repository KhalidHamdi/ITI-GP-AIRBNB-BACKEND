from rest_framework import serializers
from dj_rest_auth.serializers import LoginSerializer as DefaultLoginSerializer
from .models import User

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'avatar_url')

class CustomLoginSerializer(DefaultLoginSerializer):
    username = None  # Exclude the username field
    email = serializers.EmailField(required=True)

    def authenticate(self, **kwargs):
        from django.contrib.auth import authenticate
        return authenticate(**kwargs)

    def get_fields(self):
        fields = super().get_fields()
        fields['email'] = serializers.EmailField(required=True)
        return fields

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = self.authenticate(email=email, password=password)
            if user:
                if not user.is_active:
                    raise serializers.ValidationError('User account is disabled.')
                # Authentication successful
            else:
                raise serializers.ValidationError('Unable to log in with provided credentials.')
        else:
            raise serializers.ValidationError('Must include "email" and "password".')

        attrs['user'] = user
        return attrs
