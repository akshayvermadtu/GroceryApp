# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-12 12:21
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_auto_20180111_2208'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_time',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='order',
            name='delivery_type',
            field=models.CharField(default='cod', max_length=4),
        ),
    ]
