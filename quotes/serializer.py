from rest_framework import serializers
from .models import Quote, Product, Category

class QuoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quote
        fields = ['id', 'author_info', 'author_name', 'number_of_shares', 'quote_text']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['product_id', 'favorite_scent', 'product_link', 'product_name']

class CategorySerializer(serializers.ModelSerializer):
    product = ProductSerializer(required=False)
    quotes = QuoteSerializer(required=False)

    class Meta:
        model = Category
        fields = ['id', 'category_name', 'is_premium', 'product', 'quotes', 'wants_to_feel']
