# Generated by Django 4.0.2 on 2022-03-24 02:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auction', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='auction',
            old_name='owner',
            new_name='user',
        ),
        migrations.AddField(
            model_name='auction',
            name='note',
            field=models.TextField(blank=True, null=True),
        ),
    ]