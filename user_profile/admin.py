import django.contrib.admin.sites as admin
from django.contrib.auth.admin import UserAdmin

from .models import User, UserProfile

# Register your models here.
admin.site.register(User, UserAdmin)

# Register the UserProfile model
admin.site.register(UserProfile)