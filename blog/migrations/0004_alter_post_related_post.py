# Generated by Django 4.0.2 on 2022-03-12 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_post_related_post'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='related_post',
            field=models.ManyToManyField(blank=True, to='blog.Post'),
        ),
    ]
