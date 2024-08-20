from .models import Profile
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

class AdminLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if user and user.is_staff:
            return user
        raise serializers.ValidationError("Invalid credentials or not an admin")
    
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'user', 'balance', 'films']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']