# Generated by Django 4.0.2 on 2022-05-20 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_alter_notificationuser_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notificationuser',
            name='type',
            field=models.CharField(choices=[('GROUP_USER', 'GROUP_USER'), ('ALL_USER_AUTHENTICATED', 'ALL_USER_AUTHENTICATED'), ('ALL_USER', 'ALL_USER'), ('ONE_USER', 'ONE_USER')], max_length=22),
        ),
    ]
