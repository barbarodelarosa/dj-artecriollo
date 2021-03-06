# Generated by Django 4.0.2 on 2022-03-24 01:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='NewsletterUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('subscribe', models.BooleanField(blank=True, default=True, null=True)),
                ('unsubscribe_date', models.DateTimeField(auto_now=True, null=True)),
                ('resubscribe_date', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'ordering': ['-subscribe', '-date_added'],
            },
        ),
        migrations.CreateModel(
            name='Newsletter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('subject', models.CharField(max_length=250)),
                ('body', models.TextField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('email', models.ManyToManyField(to='newsletters.NewsletterUser')),
            ],
        ),
    ]
