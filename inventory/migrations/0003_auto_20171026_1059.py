# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-26 10:59
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_auto_20171026_1057'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventory',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2017, 10, 26, 10, 59, 28, 136029, tzinfo=utc)),
        ),
        migrations.AddField(
            model_name='inventory',
            name='last_modified',
            field=models.DateTimeField(default=datetime.datetime(2017, 10, 26, 10, 59, 28, 136053, tzinfo=utc)),
        ),
    ]
