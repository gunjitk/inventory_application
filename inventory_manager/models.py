# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=get_user_model())
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class BaseModel(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.last_modified_on = timezone.now()
        return super(BaseModel, self).save()


class InventoryUser(BaseModel):

    user = models.OneToOneField(User, related_name='inventory_user', null=True)
    is_dept_mgr = models.BooleanField(help_text="Checked if the user is department manager", default=False)
    is_store_mgr = models.BooleanField(help_text="Checked if user is store manager", default=False)
    name = models.TextField(max_length=200, default='Inventory')

    @classmethod
    def user_exists(cls, username):
        return InventoryUser.objects.filter(user__username=username).first()

    @classmethod
    def get_user_role(cls, userid):
        user = cls.objects.filter(user__id= userid)

    @classmethod
    def update_user_data(cls, user_data, user_id):

        user = cls.objects.get(user__id=user_id)
        role = user_data.get('user_role',[]).split('|')

        if role and len(role) > 0:
            user.is_dept_mgr = True if "DEPT_MGR" in role else False
            user.is_store_mgr = True if "STORE_MGR" in role else False

        user.save()

    def is_store_manager_for_inventory(self, inventory_name):

        from inventory.models import Inventory

        inventories = Inventory.objects.filter(store_manager__user=self.user).all()
        for inventory in inventories:
            if inventory.inventory_name == inventory_name:
                return True

        return False

    def __unicode__(self):  # __str__ for Python 3, __unicode__ for Python 2
        return self.name


