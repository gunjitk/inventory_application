# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-26 12:06
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0009_auto_20171026_1205'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inventoryrecords',
            name='created_on',
        ),
        migrations.RemoveField(
            model_name='inventoryrecords',
            name='last_modified',
        ),
    ]