# Generated by Django 4.0.2 on 2022-03-28 23:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_product_aprobated'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='url_short',
            field=models.SlugField(blank=True, unique=True),
        ),
    ]
