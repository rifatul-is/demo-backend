from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from quotes.models import Quote

# Create your views here.

api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_quotes(request):
    if request.method == 'GET':
        quotes = Quote.objects.all()
