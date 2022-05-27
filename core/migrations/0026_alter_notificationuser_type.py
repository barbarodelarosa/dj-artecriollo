# Generated by Django 4.0.2 on 2022-05-27 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0025_alter_notificationuser_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notificationuser',
            name='type',
            field=models.CharField(choices=[('ALL_USER_AUTHENTICATED', 'ALL_USER_AUTHENTICATED'), ('GROUP_USER', 'GROUP_USER'), ('ONE_USER', 'ONE_USER'), ('ALL_USER', 'ALL_USER')], max_length=22),
        ),
    ]
