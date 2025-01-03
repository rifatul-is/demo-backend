# Generated by Django 4.2.16 on 2024-12-16 09:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quotes', '0004_alter_category_product_alter_category_quotes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='quotes',
        ),
        migrations.AddField(
            model_name='quote',
            name='category',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='quotes', to='quotes.category'),
        ),
        migrations.AlterField(
            model_name='quote',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
