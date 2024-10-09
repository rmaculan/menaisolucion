# Generated by Django 5.1 on 2024-08-21 01:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0015_rename_user_stream_author'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='tags',
        ),
        migrations.AlterField(
            model_name='post',
            name='video',
            field=models.URLField(blank=True, default='', null=True, verbose_name='Video'),
        ),
        migrations.DeleteModel(
            name='Stream',
        ),
        migrations.DeleteModel(
            name='Tag',
        ),
    ]
