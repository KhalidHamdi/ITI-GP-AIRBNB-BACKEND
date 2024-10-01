# src/serializers.py

from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()

class UserDetailSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True, style={'input_type': 'password'}, required=False)
    password2 = serializers.CharField(write_only=True, style={'input_type': 'password'}, required=False)
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'username', 'email', 'password1', 'password2', 'id',
            'avatar', 'first_name', 'last_name', 'bio', 'address', 'phone_number'
        ]
        extra_kwargs = {
            'username': {'required': True, 'min_length': 1, 'max_length': 20},
            'email': {'required': True},
            'first_name': {'required': False, 'allow_blank': True},
            'last_name': {'required': False, 'allow_blank': True},
            'bio': {'required': False, 'allow_blank': True},
            'address': {'required': False, 'allow_blank': True},
            'phone_number': {'required': False, 'allow_blank': True},
        }

    def validate_username(self, value):
        if not value.strip():
            raise serializers.ValidationError("Username cannot be blank.")
        if len(value) > 20:
            raise serializers.ValidationError("Username cannot exceed 20 characters.")
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("A user with that username already exists.")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with that email already exists.")
        return value

    def validate(self, data):
        password1 = data.get('password1')
        password2 = data.get('password2')

        if password1 or password2:
            if not password1:
                raise serializers.ValidationError({"password1": "Password is required."})
            if not password2:
                raise serializers.ValidationError({"password2": "Password confirmation is required."})
            if password1 != password2:
                raise serializers.ValidationError({"password2": "Passwords do not match."})
        return data

    def create(self, validated_data):
        password = validated_data.pop('password1', None)
        validated_data.pop('password2', None)
        user = User.objects.create_user(**validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user

    def get_avatar(self, obj):
        return obj.avatar.url if obj.avatar else None

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username', 'email', 'avatar',
            'first_name', 'last_name', 'bio', 'address', 'phone_number'
        ]

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.bio = validated_data.get('bio', instance.bio)
        instance.address = validated_data.get('address', instance.address)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        avatar = validated_data.get('avatar', None)
        if avatar:
            instance.avatar = avatar
        instance.save()
        return instance
