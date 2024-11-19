from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from quotes.serializer import QuoteSerializer
from rest_framework.response import Response
from quotes.models import Quote
from rest_framework.views import APIView

# Create your views here.

# api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def get_quotes(request):
#     if request.method == 'GET':
#         quotes = Quote.objects.all()
#         serializer=QuoteSerializer(quotes, many=True)
#         print(serializer)
#         return Response(serializer.data)

class Quotes(APIView):
    def get(self,request):
        quotes = Quote.objects.all()
        serializer = QuoteSerializer(quotes,many =True)
        return Response (serializer.data)


