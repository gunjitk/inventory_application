# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-26 12:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0014_auto_20171026_1250'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventory',
            name='dept_managers_subscribed',
            field=models.ManyToManyField(blank=True, to='inventory_manager.InventoryUser'),
        ),
    ]
