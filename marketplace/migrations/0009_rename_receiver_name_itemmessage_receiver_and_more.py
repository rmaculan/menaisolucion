# Generated by Django 5.1.1 on 2024-10-12 03:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0008_rename_item_message_itemmessage_message'),
    ]

    operations = [
        migrations.RenameField(
            model_name='itemmessage',
            old_name='receiver_name',
            new_name='receiver',
        ),
        migrations.RenameField(
            model_name='itemmessage',
            old_name='sender_name',
            new_name='sender',
        ),
    ]
