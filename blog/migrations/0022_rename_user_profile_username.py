# Generated by Django 5.0.7 on 2024-09-07 13:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0021_alter_profile_options_alter_profile_managers_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='user',
            new_name='username',
        ),
    ]