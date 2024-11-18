from django.db import models

# Create your models here.
class Quote(models.Model):
    author_info = models.TextField(blank=True, null=True)
    author_name = models.CharField(max_length=255)
    number_of_shares = models.IntegerField(default=0)
    quote_text = models.TextField()

class Product(models.Model):
    favorite_scent = models.CharField(max_length=255, blank=True, null=False, default='')
    product_link = models.URLField(blank=True, null=False)
    product_name = models.CharField(max_length=255)

    product_id = models.CharField(max_length=200, primary_key=True, editable=False)

    def save(self, *args, **kwargs):
        self.product_id = f"{self.favorite_scent}_{self.product_name}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.favorite_scent} - {self.product_name}'

class Category(models.Model):
    category_name = models.CharField(max_length=255)
    is_premium = models.BooleanField(default=False)
    product = models.ForeignKey('Product', on_delete=models.SET_DEFAULT, related_name="category", blank=True, default=None)
    quotes = models.ForeignKey('Quote', on_delete=models.SET_DEFAULT, related_name="category", blank=True, default=None)
    wants_to_feel = models.CharField(max_length=255, blank=True, null=False, default='')