# Generated by Django 3.1.5 on 2022-06-05 11:15

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('digio', '0010_auto_20220604_2236'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectngrant',
            name='end_time',
            field=models.DateTimeField(default=datetime.datetime(2032, 1, 21, 3, 15, 29, 703533, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='projectngrant',
            name='start_time',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 6, 5, 11, 15, 29, 703448, tzinfo=utc)),
        ),
    ]
