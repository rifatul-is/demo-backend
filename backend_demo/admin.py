# admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from user_profile.models import User, UserProfile

# Register the custom User model
admin.site.register(User, UserAdmin)

# Register the UserProfile model
admin.site.register(UserProfile)
