from rest_framework import serializers
from .models import UserProfile, Category, Product, Quote
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
        


        def create(self, validated_data):
            # Automatically assign the user during creation
            request = self.context.get('request')  # Access the request from the context
            user = request.user
            validated_data['user'] = user
            return super().create(validated_data)

        def update(self, instance, validated_data):
        # If category or products are provided in the patch request, we will set them accordingly
            category_data = validated_data.get('category')
            product_data = validated_data.get('products')
            
            # You can add custom logic here to set category and products based on answers
            if category_data:
                instance.category = category_data
            if product_data:
                instance.products = product_data

            # Update other fields
            instance.name = validated_data.get('name', instance.name)
            instance.feeling_today = validated_data.get('feeling_today', instance.feeling_today)
            instance.gender = validated_data.get('gender', instance.gender)
            instance.notify_per_day = validated_data.get('notify_per_day', instance.notify_per_day)
            instance.notify_begin = validated_data.get('notify_begin', instance.notify_begin)
            instance.notify_stop = validated_data.get('notify_stop', instance.notify_stop)

            instance.save()
            return instance
