# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from inventory.models import InventoryRecords, Inventory, InventoryPermissions

admin.site.register(InventoryRecords)
admin.site.register(Inventory)
admin.site.register(InventoryPermissions)