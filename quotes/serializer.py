from rest_framework import serializers
from .models import Quote, Product, Category

class QuoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quote
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields = '__all__'


