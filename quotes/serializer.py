from rest_framework import serializers
from .models import Quote

class QuoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quote
        fields = ['author_info', 'author_name', 'number_of_shares', 'quote_text']
