# Generated by Django 4.0.2 on 2022-02-18 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0003_orderitem_stock'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='related_products',
            field=models.ManyToManyField(blank=True, null=True, to='cart.Product'),
        ),
    ]