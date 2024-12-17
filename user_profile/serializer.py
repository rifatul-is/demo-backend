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

# class UserProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserProfile
#         fields = [
#             "id",
#             "user",
#             "name",
#             "feeling_today",
#             "gender",
#             "notify_per_day",
#             "notify_begin",
#             "notify_stop",
#             "category",
#             "favorite_affirmations",
#             "past_affirmations",
#             "products"
#         ]
#         extra_kwargs = {
#             "user": {"read_only": True}  # Prevent 'user' from being required in the request data
#         }


#         def create(self, validated_data):
#             # Automatically assign the user during creation
#             request = self.context.get('request')  # Access the request from the context
#             user = request.user
#             validated_data['user'] = user
#             return super().create(validated_data)

#         def update(self, instance, validated_data):
#         # If category or products are provided in the patch request, we will set them accordingly
#             category_data = validated_data.get('category')
#             product_data = validated_data.get('products')
            
#             # You can add custom logic here to set category and products based on answers
#             if category_data:
#                 instance.category = category_data
#             if product_data:
#                 instance.products = product_data

#             # Update other fields
#             instance.name = validated_data.get('name', instance.name)
#             instance.feeling_today = validated_data.get('feeling_today', instance.feeling_today)
#             instance.gender = validated_data.get('gender', instance.gender)
#             instance.notify_per_day = validated_data.get('notify_per_day', instance.notify_per_day)
#             instance.notify_begin = validated_data.get('notify_begin', instance.notify_begin)
#             instance.notify_stop = validated_data.get('notify_stop', instance.notify_stop)

#             # Add new quotes to favorite_affirmations without overwriting
#             favorite_affirmations_ids = validated_data.get('favorite_affirmations', None)
#             if favorite_affirmations_ids is not None:
#                 quotes = Quote.objects.filter(id__in=favorite_affirmations_ids)
#                 for quote in quotes:
#                     instance.favorite_affirmations.add(quote)  # Add new items

#             # Add new quotes to past_affirmations without overwriting
#             past_affirmations_ids = validated_data.get('past_affirmations', None)
#             if past_affirmations_ids is not None:
#                 quotes = Quote.objects.filter(id__in=past_affirmations_ids)
#                 for quote in quotes:
#                     instance.past_affirmations.add(quote)  # Add new items


#             instance.save()
#             return instance

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
        extra_kwargs = {
            "user": {"read_only": True}  # Prevent 'user' from being required in the request data
        }

    def create(self, validated_data):
        # Automatically assign the user during creation
        request = self.context.get('request')  # Access the request from the context
        user = request.user
        validated_data['user'] = user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Update fields with simple assignments
        instance.name = validated_data.get('name', instance.name)
        instance.feeling_today = validated_data.get('feeling_today', instance.feeling_today)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.notify_per_day = validated_data.get('notify_per_day', instance.notify_per_day)
        instance.notify_begin = validated_data.get('notify_begin', instance.notify_begin)
        instance.notify_stop = validated_data.get('notify_stop', instance.notify_stop)
        
        # Update category and products
        category_data = validated_data.get('category')
        product_data = validated_data.get('products')
        if category_data:
            instance.category = category_data
        if product_data:
            instance.products = product_data

        # Add new quotes to favorite_affirmations without overwriting existing ones
        favorite_affirmations_ids = validated_data.get('favorite_affirmations', None)
        if favorite_affirmations_ids is not None:
            quotes = Quote.objects.filter(id__in=favorite_affirmations_ids)
            instance.favorite_affirmations.add(*quotes)  # Use bulk add to improve efficiency

        # Add new quotes to past_affirmations without overwriting existing ones
        past_affirmations_ids = validated_data.get('past_affirmations', None)
        if past_affirmations_ids is not None:
            quotes = Quote.objects.filter(id__in=past_affirmations_ids)
            instance.past_affirmations.add(*quotes)

        instance.save()
        return instance

