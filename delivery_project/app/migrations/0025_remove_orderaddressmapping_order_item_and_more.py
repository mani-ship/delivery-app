# Generated by Django 5.2.1 on 2025-07-02 09:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0024_remove_orderaddressmapping_order_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderaddressmapping',
            name='order_item',
        ),
        migrations.AddField(
            model_name='orderaddressmapping',
            name='order',
            field=models.OneToOneField(default=True, on_delete=django.db.models.deletion.CASCADE, to='app.order'),
        ),
    ]
