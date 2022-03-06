# Generated by Django 4.0.2 on 2022-03-06 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0010_alter_address_zip_code'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['-created']},
        ),
        migrations.AddField(
            model_name='product',
            name='selling',
            field=models.BooleanField(default=False),
        ),
    ]
