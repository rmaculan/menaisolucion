# Generated by Django 5.1.1 on 2024-10-15 23:28

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0013_alter_itemroom_item_alter_itemroom_seller'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
