# Generated by Django 4.0.2 on 2022-02-05 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0002_product_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.IntegerField(default=0),
        ),
    ]