# Generated by Django 5.0.7 on 2024-08-05 06:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_register_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Login',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('host', models.CharField(max_length=50, unique=True)),
                ('email', models.CharField(max_length=30, unique=True)),
                ('password', models.CharField(max_length=20)),
            ],
        ),
    ]
