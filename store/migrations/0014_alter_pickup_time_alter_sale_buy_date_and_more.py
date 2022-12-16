# Generated by Django 4.0.4 on 2022-12-16 06:23

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0013_alter_pickup_time_alter_sale_buy_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pickup',
            name='time',
            field=models.TimeField(default=datetime.datetime(2022, 12, 16, 6, 23, 4, 26316, tzinfo=utc), help_text='Hora de recogida del tour', verbose_name='Hora de recogida'),
        ),
        migrations.AlterField(
            model_name='sale',
            name='buy_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 16, 6, 23, 4, 27318, tzinfo=utc), help_text='Fecha de inicio de la venta', verbose_name='Fecha de venta'),
        ),
        migrations.AlterField(
            model_name='sale',
            name='tour_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 16, 6, 23, 4, 27318, tzinfo=utc), help_text='Fecha del tour', verbose_name='Fecha'),
        ),
        migrations.AlterField(
            model_name='tour',
            name='date_end',
            field=models.DateField(default=datetime.datetime(2022, 12, 16, 6, 23, 3, 905316, tzinfo=utc), help_text='Fecha de fin del tour', verbose_name='Fecha de fin'),
        ),
        migrations.AlterField(
            model_name='tour',
            name='date_start',
            field=models.DateField(default=datetime.datetime(2022, 12, 16, 6, 23, 3, 905316, tzinfo=utc), help_text='Fecha de inicio del tour', verbose_name='Fecha de inicio'),
        ),
        migrations.AlterField(
            model_name='tourtime',
            name='time_start',
            field=models.TimeField(default=datetime.datetime(2022, 12, 16, 6, 23, 4, 25317, tzinfo=utc), help_text='Hora de inicio del tour', verbose_name='Hora de inicio'),
        ),
    ]
