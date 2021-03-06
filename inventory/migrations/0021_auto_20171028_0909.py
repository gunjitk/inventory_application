# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-28 09:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0020_auto_20171026_1846'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventorypermissions',
            name='status',
            field=models.CharField(default='Pending', max_length=20),
        ),
        migrations.AlterField(
            model_name='inventory',
            name='total_items',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='inventoryrecords',
            name='batch_date',
            field=models.CharField(default=b'2017-10-28', help_text='must be in format yyyy-mm-dd', max_length=100, null=True),
        ),
    ]
