from django.contrib import admin
from .models import Category, Product, Quote

# Register your models here.
admin.site.register(Category)
admin.site.register(Quote)
admin.site.register(Product)
