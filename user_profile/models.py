from django.contrib.auth.models import AbstractUser
from django.db import models
from quotes.models import Quote, Category, Product

# Custom User Manager
# class CustomUserManager(BaseUserManager):
#     def create_user(self, email, password=None, **extra_fields):
#         if not email:
#             raise ValueError("The Email field must be set")
#         email = self.normalize_email(email)
#         user = self.model(email=email, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user
#
#     def create_superuser(self, email, password=None, **extra_fields):
#         extra_fields.setdefault("is_staff", True)
#         extra_fields.setdefault("is_superuser", True)
#
#         if not extra_fields.get("is_staff"):
#             raise ValueError("Superuser must have is_staff=True.")
#         if not extra_fields.get("is_superuser"):
#             raise ValueError("Superuser must have is_superuser=True.")
#
#         return self.create_user(email, password, **extra_fields)


# User Model
class User(AbstractUser):
    email = models.EmailField(unique=True, max_length=255)

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

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    name = models.CharField(max_length=255)
    feeling_today = models.CharField(max_length=255)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default="O")
    notify_per_day = models.IntegerField(default=1)
    notify_begin = models.BooleanField(blank=True, default=False)
    notify_stop = models.BooleanField(blank=True, default=False)
    category = models.OneToOneField(
        Category, on_delete=models.SET_DEFAULT, blank=True, null=True, default=None, related_name="user_profile"
    )
    favorite_affirmations = models.ForeignKey(
        Quote, on_delete=models.SET_DEFAULT, blank=True, null=True, default=None, related_name="favorited_profiles"
    )
    past_affirmations = models.ForeignKey(
        Quote, on_delete=models.SET_DEFAULT, blank=True, null=True, default=None, related_name="past_profiles"
    )
    products = models.ForeignKey(
        Product, on_delete=models.SET_DEFAULT, blank=True, null=True, default=None, related_name="user_profiles"
    )

    def __str__(self):
        return f"Profile of {self.user.email}"
