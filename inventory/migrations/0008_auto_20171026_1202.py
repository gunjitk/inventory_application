# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-26 12:02
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0007_auto_20171026_1130'),
    ]

    operations = [
        migrations.CreateModel(
            name='InventoryRecords',
            fields=[
                ('id', models.IntegerField(default=0, primary_key=True, serialize=False)),
                ('product_id', models.IntegerField(default=0)),
                ('product_name', models.CharField(max_length=200)),
                ('Vendor', models.CharField(max_length=200)),
                ('MRP', models.IntegerField(null=True)),
                ('batch_num', models.IntegerField(null=True)),
                ('batch_date', models.DateField(default=datetime.date(2017, 10, 26))),
                ('Quantity', models.IntegerField(null=True)),
                ('status', models.CharField(default='PENDING', max_length=200)),
                ('created_on', models.DateTimeField(default=datetime.datetime(2017, 10, 26, 12, 2, 42, 213190, tzinfo=utc))),
                ('last_modified', models.DateTimeField(default=datetime.datetime(2017, 10, 26, 12, 2, 42, 213267, tzinfo=utc))),
                ('inventory', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='inventory', to='inventory.Inventory')),
            ],
        ),
        migrations.RemoveField(
            model_name='inventoryrecord',
            name='inventory',
        ),
        migrations.DeleteModel(
            name='InventoryRecord',
        ),
    ]
