# Generated by Django 5.2 on 2025-07-22 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_product_discount_percentage_product_has_discount_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='img_url',
            field=models.URLField(blank=True, max_length=500, null=True),
        ),
    ]
