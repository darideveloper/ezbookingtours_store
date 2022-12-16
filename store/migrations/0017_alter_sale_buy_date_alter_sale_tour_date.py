# Generated by Django 4.0.4 on 2022-12-16 06:33

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0016_alter_pickup_time_alter_sale_buy_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sale',
            name='buy_date',
            field=models.DateTimeField(default=django.utils.timezone.now, help_text='Fecha de venta', verbose_name='Fecha venta'),
        ),
        migrations.AlterField(
            model_name='sale',
            name='tour_date',
            field=models.DateTimeField(default=django.utils.timezone.now, help_text='Fecha del tour', verbose_name='Fecha tour'),
        ),
    ]
