# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-26 18:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0019_auto_20171026_1822'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventoryrecords',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]