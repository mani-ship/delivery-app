# Generated by Django 5.1.1 on 2025-06-05 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_product_discount_price_delete_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='quantity',
            field=models.CharField(choices=[('1kg', '1 Kg'), ('500g', '500 Grams'), ('2kg', '2kg'), ('3kg', '3kg'), ('4kg', '4kg'), ('5kg', '5kg')], default='500g', max_length=20),
        ),
    ]
