from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError



User = get_user_model()

class UserDetailSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, style={'input_type': 'password'})
    avatar = serializers.SerializerMethodField()


    class Meta:
        model = User

        fields = ['username', 'email', 'password1', 'password2', 'id' , 'avatar']
        extra_kwargs = {
            'username': {'required': True, 'min_length': 1, 'max_length': 20},
            'email': {'required': True},
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
        if data['password1'] != data['password2']:
            raise serializers.ValidationError({"password2": "Passwords do not match."})
        return data

    def create(self, validated_data):
        password = validated_data.pop('password1')
        validated_data.pop('password2')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=password
        )
        return user
    
    def get_avatar(self, obj):
        return obj.avatar.url if obj.avatar else None

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'avatar']  

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        avatar = validated_data.get('avatar', None)
        if avatar:
            instance.avatar = avatar
        instance.save()
        return instance
