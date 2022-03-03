# Generated by Django 4.0.2 on 2022-03-03 20:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authy', '0006_profile_phone'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='banner',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='picture',
        ),
        migrations.AddField(
            model_name='profile',
            name='first_name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='last_name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
