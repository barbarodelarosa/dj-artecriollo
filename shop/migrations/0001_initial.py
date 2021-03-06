# Generated by Django 4.0.2 on 2022-03-24 01:56

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import shop.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('localidad', models.CharField(blank=True, max_length=25, null=True)),
                ('address_line_1', models.CharField(max_length=150)),
                ('address_line_2', models.CharField(max_length=150)),
                ('numero', models.CharField(max_length=8)),
                ('apt', models.CharField(max_length=5)),
                ('city', models.CharField(max_length=150)),
                ('address_type', models.CharField(choices=[('P', 'Particular'), ('E', 'Envio')], max_length=1)),
                ('default', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name_plural': 'Addresses',
                'ordering': ['provincia', 'municipio'],
            },
        ),
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='image/category')),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(blank=True, null=True, unique=True)),
                ('active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='ColorVariation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='MaterialVariation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Merchant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('slug', models.SlugField(blank=True, max_length=25, null=True, unique=True)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='image/merchant')),
                ('image', models.ImageField(blank=True, null=True, upload_to='image/merchant')),
                ('banner', models.ImageField(blank=True, null=True, upload_to='image/merchant')),
                ('description', ckeditor.fields.RichTextField()),
                ('phone', models.CharField(blank=True, max_length=11, null=True)),
                ('address', models.CharField(blank=True, max_length=125, null=True)),
                ('status', models.BooleanField(default=False)),
                ('public', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField(auto_now_add=True)),
                ('ordered_date', models.DateTimeField(blank=True, null=True)),
                ('ordered', models.BooleanField(default=False)),
                ('shipping', models.IntegerField(default=0)),
                ('discount', models.IntegerField(default=0)),
                ('status', models.CharField(blank=True, choices=[('CONFIRMADO', 'CONFIRMADO'), ('EN PREPARACI??N', 'EN PREPARACI??N'), ('PREPARADO', 'PREPARADO'), ('ENTREGADO', 'ENTREGADO'), ('ANULADO', 'ANULADO')], max_length=15, null=True)),
                ('pay_status', models.CharField(blank=True, choices=[('NO PAGADO', 'NO PAGADO'), ('AUTORIZADO', 'AUTORIZADO'), ('PAGADO', 'PAGADO'), ('ANULADO', 'ANULADO')], max_length=15, null=True)),
                ('note', models.TextField(blank=True, null=True)),
                ('first_name', models.CharField(blank=True, max_length=25, null=True)),
                ('last_name', models.CharField(blank=True, max_length=25, null=True)),
                ('phone', models.CharField(blank=True, max_length=12, null=True)),
                ('email', models.EmailField(blank=True, max_length=25, null=True)),
                ('payment_method', models.CharField(choices=[('EFECTIVO', 'EFECTIVO'), ('ENZONA', 'ENZONA'), ('TRANSFERMOVIL', 'TRANSFERMOVIL')], default='EFECTIVO', max_length=25)),
                ('billing_address', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='billing_address', to='shop.address')),
                ('shipping_address', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='shipping_address', to='shop.address')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Pais',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Cuba', max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('image', models.ImageField(upload_to=shop.models.user_directory_path)),
                ('price', models.IntegerField(default=0)),
                ('old_price', models.IntegerField(blank=True, default=0, null=True)),
                ('description', models.TextField()),
                ('details', ckeditor.fields.RichTextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=False)),
                ('stock', models.PositiveIntegerField(default=0)),
                ('new', models.BooleanField(default=True)),
                ('selling', models.BooleanField(default=False)),
                ('digital', models.BooleanField(default=False)),
                ('content_url', models.URLField(blank=True, null=True)),
                ('content_file', models.FileField(blank=True, null=True, upload_to='products/content-files/')),
                ('for_auction', models.BooleanField(default=False)),
                ('close_auction', models.DateTimeField(auto_now=True)),
                ('selling_date', models.DateTimeField(auto_now=True)),
                ('avialable_colours', models.ManyToManyField(blank=True, to='shop.ColorVariation')),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='SizeVariation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name_plural': 'Tags',
            },
        ),
        migrations.CreateModel(
            name='WhishList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=150, null=True)),
                ('products', models.ManyToManyField(blank=True, related_name='products_whishlist', to='shop.Product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='whishlist_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PurchasedProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('date_purchased', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.product')),
            ],
        ),
        migrations.CreateModel(
            name='Provincia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=15)),
                ('pais', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.pais')),
            ],
        ),
        migrations.CreateModel(
            name='ProductImagesContent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to=shop.models.user_directory_path)),
                ('posted', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='content_owner', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='avialable_sizes',
            field=models.ManyToManyField(blank=True, to='shop.SizeVariation'),
        ),
        migrations.AddField(
            model_name='product',
            name='brand',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.brand'),
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ManyToManyField(to='shop.Category'),
        ),
        migrations.AddField(
            model_name='product',
            name='merchant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.merchant'),
        ),
        migrations.AddField(
            model_name='product',
            name='product_images',
            field=models.ManyToManyField(blank=True, related_name='images_product', to='shop.ProductImagesContent'),
        ),
        migrations.AddField(
            model_name='product',
            name='related_products',
            field=models.ManyToManyField(blank=True, to='shop.Product'),
        ),
        migrations.AddField(
            model_name='product',
            name='tag',
            field=models.ManyToManyField(blank=True, to='shop.Tag'),
        ),
        migrations.AddField(
            model_name='product',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_method', models.CharField(choices=[('Paypal', 'Paypal'), ('ENZONA', 'ENZONA')], max_length=20)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('successfull', models.BooleanField(default=False)),
                ('amount', models.FloatField()),
                ('raw_response', models.TextField()),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='shop.order')),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('tax', models.IntegerField(default=0)),
                ('discount', models.IntegerField(default=0)),
                ('stock', models.PositiveIntegerField(default=0)),
                ('colour', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.colorvariation')),
                ('material', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.materialvariation')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='shop.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.product')),
                ('shop', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.shop')),
                ('size', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.sizevariation')),
            ],
        ),
        migrations.CreateModel(
            name='Municipio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=15)),
                ('pais', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.pais')),
                ('provincia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.provincia')),
            ],
        ),
        migrations.AddField(
            model_name='address',
            name='municipio',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.municipio'),
        ),
        migrations.AddField(
            model_name='address',
            name='pais',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.pais'),
        ),
        migrations.AddField(
            model_name='address',
            name='provincia',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.provincia'),
        ),
        migrations.AddField(
            model_name='address',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
