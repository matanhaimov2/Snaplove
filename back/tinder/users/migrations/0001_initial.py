# Generated by Django 5.0.7 on 2024-08-08 05:23

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(default='default@example.com', max_length=254)),
                ('username', models.CharField(default='default_username', max_length=150)),
                ('first_name', models.CharField(default='default_firstname', max_length=150)),
                ('last_name', models.CharField(default='default_lastname', max_length=150)),
                ('isFirstLogin', models.BooleanField(default=True)),
                ('gender', models.CharField(blank=True, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], max_length=10, null=True)),
                ('age', models.IntegerField(blank=True, null=True)),
                ('interested_in', models.CharField(blank=True, max_length=100)),
                ('location', models.CharField(blank=True, max_length=255)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'users_profile',
            },
        ),
    ]
