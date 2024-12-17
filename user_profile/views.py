from django.http import JsonResponse
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from user_profile.models import UserProfile
from quotes.models import Quote, Category
from user_profile.serializer import UserProfileSerializer

User = get_user_model()

@api_view(['POST'])
def create_user(request):
    if request.method == 'POST':
        # Accessing data from request.data for JSON payload
        email = request.data.get('email')
        username = request.data.get('username')
        password = request.data.get('password')

        # Check if all required fields are present
        if not email or not username or not password:
            return JsonResponse({'error': 'All fields are required'}, status=400)

        # Check if user with the provided email already exists
        if User.objects.filter(email=email).exists():
            return JsonResponse({'error': 'Email is already in use'}, status=400)

        # Create the new user
        user = User.objects.create_user(email=email, username=username, password=password)

        #UserProfile.objects.create(user=user)

        # Return success response
        return JsonResponse({'message': 'User created successfully'}, status=201)

    # If the method is not POST
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_user_profiles(request):
    if request.method == 'GET':
        user_profiles = UserProfile.objects.all()
        serializer = UserProfileSerializer(user_profiles, many=True)
        return Response(serializer.data)

# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def create_user_profile(request):
#     if request.method == 'POST':
#         serializer = UserProfileSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_user_profile(request):
    if request.method == 'POST':
        # Make a copy of request data and add the user field
        data = request.data.copy()
        data['user'] = request.user.id  # Auto-assign the user

        # Pass the updated data to the serializer
        serializer = UserProfileSerializer(data=data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_user_profile(request):
    try:
        # Get the user profile for the currently logged-in user
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        return Response({"error": "User profile not found"}, status=status.HTTP_404_NOT_FOUND)

    # Serialize the data, allowing partial updates (i.e., fields that are provided in the request)
    serializer = UserProfileSerializer(user_profile, data=request.data, partial=True)
    
    if serializer.is_valid():
        # Save the updated instance and return the response
        serializer.save()
        return Response({"message": "Profile updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_affirmations(request):
    try:
        # Get the authenticated user
        user = request.user

        # Get the user profile
        user_profile = UserProfile.objects.get(user=user)

        # Get current affirmations to preserve them
        current_favorite_ids = list(user_profile.favorite_affirmations.all())
        current_past_ids = list(user_profile.past_affirmations.all())
        print('current_favorite_ids',current_favorite_ids)
        print('current_past_ids',current_past_ids)

        # Get new IDs from the request payload
        new_favorite_ids = request.data.get('favorite', [])
        new_past_ids = request.data.get('past', [])

        print('new_favorite_ids',new_favorite_ids)
        print('new_past_ids',new_past_ids)

        # Combine previous IDs with new ones (avoiding duplicates)
        updated_favorite_ids = list(set(current_favorite_ids + new_favorite_ids))
        updated_past_ids = list(set(current_past_ids + new_past_ids))
        print('updated_favorite_ids',updated_favorite_ids)
        print('updated_past_ids',updated_past_ids)

        # Validate the quote IDs
        if new_favorite_ids:
            quotes = Quote.objects.filter(id__in=new_favorite_ids)
            if len(quotes) != len(new_favorite_ids):
                return Response({"detail": "Some favorite quote IDs are invalid."}, status=status.HTTP_400_BAD_REQUEST)

        if new_past_ids:
            quotes = Quote.objects.filter(id__in=new_past_ids)
            if len(quotes) != len(new_past_ids):
                return Response({"detail": "Some past quote IDs are invalid."}, status=status.HTTP_400_BAD_REQUEST)

        # Update profile affirmations
        user_profile.favorite_affirmations.set(updated_favorite_ids)
        user_profile.past_affirmations.set(updated_past_ids)
        user_profile.save()

        # Return updated data
        serializer = UserProfileSerializer(user_profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except UserProfile.DoesNotExist:
        return Response({"detail": "User profile not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

   

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def remove_affirmation(request):
    try:
        # Get the authenticated user
        user = request.user

        # Get the user profile
        user_profile = UserProfile.objects.get(user=user)

        # Get the affirmation ID and type (favorite or past) from request data
        affirmation_id = request.data.get('affirmation_id')
        list_type = request.data.get('list_type')  # 'favorite' or 'past'

        # Validate input
        if not affirmation_id or not list_type:
            return Response(
                {"detail": "'affirmation_id' and 'list_type' are required fields."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Verify that the quote exists
            quote = Quote.objects.get(id=affirmation_id)
        except Quote.DoesNotExist:
            return Response({"detail": "Quote not found."}, status=status.HTTP_404_NOT_FOUND)

        # Remove the quote from the appropriate list
        if list_type == 'favorite':
            if quote in user_profile.favorite_affirmations.all():
                user_profile.favorite_affirmations.remove(quote)
                return Response({"detail": f"Quote {affirmation_id} removed from favorite list."}, status=status.HTTP_200_OK)
            else:
                return Response({"detail": "Quote not in favorite list."}, status=status.HTTP_400_BAD_REQUEST)

        elif list_type == 'past':
            if quote in user_profile.past_affirmations.all():
                user_profile.past_affirmations.remove(quote)
                return Response({"detail": f"Quote {affirmation_id} removed from past list."}, status=status.HTTP_200_OK)
            else:
                return Response({"detail": "Quote not in past list."}, status=status.HTTP_400_BAD_REQUEST)
        
        else:
            return Response({"detail": "Invalid 'list_type'. Use 'favorite' or 'past'."}, status=status.HTTP_400_BAD_REQUEST)

    except UserProfile.DoesNotExist:
        return Response({"detail": "User profile not found."}, status=status.HTTP_404_NOT_FOUND)
