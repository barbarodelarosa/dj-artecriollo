# Generated by Django 4.0.2 on 2022-05-27 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0015_alter_address_address_line_1_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='municipio',
            name='shipping',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]
