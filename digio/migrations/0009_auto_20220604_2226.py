# Generated by Django 3.1.5 on 2022-06-04 22:26

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('digio', '0008_auto_20220604_2144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectngrant',
            name='end_time',
            field=models.DateTimeField(default=datetime.datetime(2032, 1, 20, 14, 26, 28, 430095, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='projectngrant',
            name='start_time',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 6, 4, 22, 26, 28, 430058, tzinfo=utc)),
        ),
    ]
