# Generated by Django 4.0.2 on 2022-05-21 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lottery', '0003_alter_participantpayment_transaction_uuid_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lottery',
            name='price_lottery',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=6, verbose_name='Monto de inscripción'),
        ),
    ]