# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-26 12:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0013_inventory_dept_managers_subscribed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventory',
            name='dept_managers_subscribed',
            field=models.ManyToManyField(null=True, to='inventory_manager.InventoryUser'),
        ),
    ]
