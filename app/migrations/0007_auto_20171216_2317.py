# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-16 17:47
from __future__ import unicode_literals

from django.db import migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_order_item_list'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='cart',
            field=jsonfield.fields.JSONField(),
        ),
    ]
