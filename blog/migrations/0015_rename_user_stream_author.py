# Generated by Django 5.1 on 2024-08-16 21:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0014_comment_parent'),
    ]

    operations = [
        migrations.RenameField(
            model_name='stream',
            old_name='user',
            new_name='author',
        ),
    ]
