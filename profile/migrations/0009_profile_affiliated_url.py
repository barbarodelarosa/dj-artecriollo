# Generated by Django 4.0.2 on 2022-04-05 21:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0008_alter_profile_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='affiliated_url',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
