# Generated by Django 4.0.2 on 2022-03-25 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0002_profile_code_profile_recommended_by_profile_updated_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='gender',
            field=models.CharField(blank=True, choices=[('HOMBRE', 'HOMBRE'), ('MUJER', 'MUJER'), ('OTRO', 'OTRO')], max_length=6, null=True),
        ),
    ]