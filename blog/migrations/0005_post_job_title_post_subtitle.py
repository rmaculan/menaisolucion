# Generated by Django 5.0.7 on 2024-08-05 03:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_alter_post_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='job_title',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='post',
            name='subtitle',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
