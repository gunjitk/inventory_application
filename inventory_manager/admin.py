# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from inventory_manager.models import InventoryUser

admin.site.register(InventoryUser)
