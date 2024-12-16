from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from quotes.serializer import QuoteSerializer
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from quotes.models import Quote, Category
from user_profile.models import UserProfile
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

# class Quotes(APIView):
#     def get(self,request):
#         quotes = Quote.objects.all()
#         serializer = QuoteSerializer(quotes,many =True)
#         return Response (serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def quotes_by_user_category(request):
    """
    Get a list of quotes based on the user's category, paginated.
    """
    # Step 1: Retrieve the user's category
    user = request.user
    user_profile = UserProfile.objects.filter(user=request.user).first()
    if not user_profile:
        return Response({"error": "User profile is not defined."}, status=400)
    if not user_profile.category:
        return Response({"error": "User category is not defined."}, status=400)


    category = user_profile.category

    # Step 2: Filter quotes related to the user's category
    quotes = Quote.objects.filter(category__id=category.id)

    # Step 3: Paginate the quotes
    paginator = PageNumberPagination()
    paginated_quotes = paginator.paginate_queryset(quotes, request)

    # Step 4: Serialize and return the response
    serializer = QuoteSerializer(paginated_quotes, many=True)
    return paginator.get_paginated_response(serializer.data)

