# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime
from django.db import models

# Create your models here.
from django.utils import timezone

from inventory_manager.models import InventoryUser
from django.db.models import Q


class Inventory(models.Model):

    inventory_name = models.CharField(max_length=200, unique=True)
    store_manager = models.ForeignKey(InventoryUser, related_name="store_manager_id",
                                      limit_choices_to={'is_store_mgr': True})
    total_items = models.IntegerField(default=0, null=True)
    dept_managers_subscribed = models.ManyToManyField(InventoryUser, limit_choices_to={'is_dept_mgr':True}, blank=True)

    @classmethod
    def get_all_inventories(cls, user):
            return cls.objects.filter(Q(store_manager = user) | Q(dept_managers_subscribed=user)).distinct().all()

    @classmethod
    def is_user_permitted(cls, user):
        return cls.objects.filter(dept_managers_subscribed=user).exists()

    def user_can_add_record_to_inventory(self, inventory_user):
        if inventory_user.is_store_manager_for_inventory(self.inventory_name):
            return True
        elif inventory_user.user.user_permissions.filter(codename='can_add_record_to_%s'%self.inventory_name).exists():
            return True

        return False

    def user_can_delete_record_from_inventory(self, inventory_user):
        if inventory_user.is_store_manager_for_inventory(self.inventory_name):
            return True
        elif inventory_user.user.user_permissions.filter(codename='can_delete_record_from_%s'%self.inventory_name).exists():
            return True

        return False

    def user_can_edit_record_of_inventory(self, inventory_user):
        if inventory_user.is_store_manager_for_inventory(self.inventory_name):
            return True
        elif inventory_user.user.user_permissions.filter(codename='can_edit_record_of_%s'%self.inventory_name).exists():
            return True

        return False

    def __unicode__(self):
        return "%s" %self.inventory_name

class InventoryRecords(models.Model):

    product_id = models.IntegerField(default=0)
    product_name = models.CharField(max_length=200, unique=True)
    Vendor = models.CharField(max_length=200)
    MRP = models.IntegerField(null=True)
    batch_num = models.IntegerField(null=True)
    batch_date = models.CharField(null=True, default=str(timezone.now().date()), max_length=100, help_text="must be in format yyyy-mm-dd")
    Quantity = models.IntegerField(null=True)
    status = models.CharField(max_length=200, default="PENDING")
    inventory = models.ForeignKey(Inventory, related_name="inventory", null=True)

    def __unicode__(self):
        return "%s" % self.product_name

    @classmethod
    def get_inventory_records_data(cls, inventory):
        return [record for record in cls.objects.filter(inventory = inventory).values()]


class InventoryPermissions(models.Model):

    store_manager = models.ForeignKey(InventoryUser, related_name="store_manager",
                                      limit_choices_to={'is_store_mgr': True})
    inventory_name = models.CharField(max_length=200, null=True)
    permission_codename = models.CharField(max_length=200, null=True)
    target_user = models.CharField(max_length=200, null=True)
    status = models.CharField(default='Pending', max_length=20)

