# Generated by Django 5.0.7 on 2024-10-11 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interactions', '0015_imageupload'),
    ]

    operations = [
        migrations.AddField(
            model_name='imageupload',
            name='room_id',
            field=models.CharField(default=None, max_length=255, unique=True),
        ),
    ]
