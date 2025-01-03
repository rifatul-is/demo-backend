# Generated by Django 4.2.16 on 2024-12-17 07:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quotes', '0005_remove_category_quotes_quote_category_alter_quote_id'),
        ('user_profile', '0003_alter_userprofile_favorite_affirmations'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='category',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='user_profile', to='quotes.category'),
        ),
    ]
