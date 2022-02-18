# Generated by Django 4.0.2 on 2022-02-18 20:12

import cart.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cart', '0005_alter_product_related_products'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductImagesContent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to=cart.models.user_directory_path)),
                ('posted', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_image_content', to='cart.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='content_owner', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='product_images',
            field=models.ManyToManyField(blank=True, related_name='images_product', to='cart.ProductImagesContent'),
        ),
    ]
