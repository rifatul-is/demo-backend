from django.http import JsonResponse
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from user_profile.models import UserProfile
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
