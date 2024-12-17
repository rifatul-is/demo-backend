from django.urls import path
from .views import create_user, create_user_profile, update_user_profile, update_affirmations, remove_affirmation
from rest_framework_simplejwt.views import (TokenObtainPairView)

urlpatterns = [
    path("register/", create_user , name="create_user"),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path("profile/", create_user_profile , name="create_user_profile"),
    path("update_profile/", update_user_profile , name="update_user_profile"),
    path('update_affirmations/', update_affirmations, name='update_affirmations'),
    path('remove_affirmation/',remove_affirmation,name="remove_affirmation"),


]