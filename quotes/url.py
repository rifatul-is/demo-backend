from django.urls import path
from .views import Quotes


urlpatterns = [
    path("get_quotes/", Quotes.as_view() , name="get_quotes"),
    # path('get_quotes/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
   # path("profile/", create_user , name="create_user_profile"),
]