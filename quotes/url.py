from django.urls import path
from .views import quotes_by_user_category


urlpatterns = [
    path('get_quotes/', quotes_by_user_category, name='quotes-by-user-category'),

    #path("get_quotes/", Quotes.as_view() , name="get_quotes"),
    # path('get_quotes/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
   # path("profile/", create_user , name="create_user_profile"),
]