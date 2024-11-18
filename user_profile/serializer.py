from rest_framework import serializers
from .models import UserProfile
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'username', 'password']
        extra_kwargs = {
            'password': {'write_only': True}  # Make sure password is not included in responses
        }

    def create(self, validated_data):
        # This will create a user with hashed password
        user = User.objects.create_user(**validated_data)
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            "id",
            "user",
            "name",
            "feeling_today",
            "gender",
            "notify_per_day",
            "notify_begin",
            "notify_stop",
            "category",
            "favorite_affirmations",
            "past_affirmations",
            "products"
        ]
        read_only_fields = ["user"]
