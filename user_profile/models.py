from django.contrib.auth.models import AbstractUser
from django.db import models
from quotes.models import Quote, Category, Product

# User Model
class User(AbstractUser):
    email = models.EmailField(unique=True, max_length=255)
    username = models.CharField(max_length=255,blank=True,null=True)

    # Ensures email is used as the unique identifier for login
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email


# User Profile Model
class UserProfile(models.Model):
    GENDER_CHOICES = [
        ("M", "Male"),
        ("F", "Female"),
        ("O", "Other"),
    ]

    user = models.OneToOneField(User,default=None,null=True, on_delete=models.CASCADE, related_name="profile")
    name = models.CharField(max_length=255)
    feeling_today = models.CharField(max_length=255)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default="O")
    notify_per_day = models.IntegerField(default=1)
    notify_begin = models.IntegerField(blank=True, default=10)
    notify_stop = models.IntegerField(blank=True, default=12)
    category = models.ForeignKey(
        Category, on_delete=models.SET_DEFAULT, blank=True, null=True, default=None, related_name="user_profile"
    )
    favorite_affirmations = models.ManyToManyField(
        Quote, blank=True, null=True, related_name="favorited_profiles"
    ) 
    past_affirmations = models.ManyToManyField(
        Quote, blank=True, null=True, default=None, related_name="past_profiles"
    )
    products = models.ForeignKey(
        Product, on_delete=models.SET_DEFAULT, blank=True, null=True, default=None, related_name="user_profiles"
    )

    def __str__(self):
        if self.user:
            return f"Profile of {self.user.email}"
        return "Profile of Unknown User"
