from django.urls import path
from .views import create_user
from rest_framework_simplejwt.views import (TokenObtainPairView)

urlpatterns = [
    path("register/", create_user , name="create_user"),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path("profile/", create_user , name="create_user"),
]