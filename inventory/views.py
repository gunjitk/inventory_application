# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from rest_framework.authentication import TokenAuthentication
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN
from rest_framework.views import APIView

from inventory.models import Inventory, InventoryRecords, InventoryPermissions
from inventory_manager.models import InventoryUser
from django.contrib.auth.models import Permission


class InventoryView(APIView):
    authentication_classes = (TokenAuthentication,)

    def get(self, request, **kwargs):

        show_all_inventories = request.GET.get('show_all','')
        user = request.user
        list_of_inventories = []
        status = HTTP_200_OK

        try:
            inventory_user = InventoryUser.user_exists(username=user.username)
            user_permitted = Inventory.is_user_permitted(user=inventory_user)

            if show_all_inventories == "true":

                users_inventories = Inventory.objects.values()
                for inventory in users_inventories:
                    inventory_dict = {}
                    inventory_dict[inventory['inventory_name']] = inventory
                    list_of_inventories.append(inventory_dict)

            elif inventory_user.is_store_mgr or user_permitted:

                users_inventories = Inventory.get_all_inventories(user=inventory_user)
                for inventory in users_inventories:
                    inventory_dict = {}
                    inventory_records = InventoryRecords.get_inventory_records_data(inventory=inventory)
                    inventory_dict[inventory.inventory_name] = inventory_records
                    list_of_inventories.append(inventory_dict)

        except Exception as e:
            status = HTTP_400_BAD_REQUEST
            list_of_inventories.append({'error':"Can't fetch all records"})

        return HttpResponse(json.dumps(list_of_inventories), status=status, content_type='application/json')

    def post(self, request):

        user = request.user
        request_data = json.loads(request.body)
        subscribe_to = request_data.get('subscribe_to')
        inventory_user = InventoryUser.user_exists(username=user.username)
        status = HTTP_200_OK
        response = []

        try:
            inventory = Inventory.objects.filter(inventory_name=subscribe_to).first()
            if inventory:
                inventory.dept_managers_subscribed.add(inventory_user)
                response.append({'success': True})

        except Exception as e:
            status = HTTP_400_BAD_REQUEST
            response.append({'error': 'Inventory does not exist'})

        return HttpResponse(json.dumps(response), status=status, content_type='application/json')




class InventoryPermissionView(APIView):

    authentication_classes = (TokenAuthentication,)

    def get(self, request):

        user = request.user
        status = HTTP_200_OK
        permissions = []

        try:
            inventory_user = InventoryUser.user_exists(username=user.username)
            if inventory_user.is_store_mgr:
                to_be_approved_permissions = InventoryPermissions.objects.filter(store_manager=inventory_user).values()
                for permission in to_be_approved_permissions:
                    permissions.append(permission)

        except Exception as e:
            status = HTTP_400_BAD_REQUEST
            permissions.append({'error': 'Cant fetch all permissions'})

        return HttpResponse(json.dumps(permissions), status=status, content_type='application/json')

    def post(self, request, **kwargs):

        user = request.user
        user_data = json.loads(request.body)
        status = HTTP_200_OK
        permission_name = user_data.get('permission_name')
        inventory_name = user_data.get('inventory_name')
        target_user = user_data.get('to_username')

        response = []

        try:
            inventory_user = InventoryUser.user_exists(username=user.username)
            target_user = InventoryUser.user_exists(username=target_user)

            if inventory_user.is_store_manager_for_inventory(inventory_name):
                permission_object = Permission.objects.filter(codename=permission_name, user=target_user.user)
                if not permission_object:
                    content_type = ContentType.objects.get_for_model(InventoryRecords)
                    permission_object = Permission.objects.get_or_create(codename=permission_name, name=permission_name, content_type=content_type)[0]
                    target_user.user.user_permissions.add(permission_object)
                    InventoryPermissions.objects.filter(permission_codename=permission_name, target_user=target_user.user.username).delete()
                    response.append({'success': 'Given permission to user'})
                else:
                    response.append({'success': 'user already has permission'})

            else:
                status = HTTP_403_FORBIDDEN
                response.append({'error': 'Cant give permission'})


        except Exception as e:
            status = HTTP_400_BAD_REQUEST
            response.append({'error': 'Some error occured in processing the request'})

        return HttpResponse(json.dumps(response), status=status, content_type='application/json')


class InventoryUpdateView(APIView):
    authentication_classes = (TokenAuthentication,)

    def post(self, request):

        user = request.user
        user_data = json.loads(request.body)
        inventory_user = InventoryUser.user_exists(username=user.username)
        inventory_name = user_data.get('inventory_name')
        inventory_record = user_data.get('inventory_record')
        status = HTTP_200_OK
        response = []
        try:
            inventory_object = Inventory.objects.filter(inventory_name=inventory_name).first()

            if inventory_object.user_can_add_record_to_inventory(inventory_user):

                inventory_record = InventoryRecords(product_id=inventory_record.get('product_id'),
                                                    product_name=inventory_record.get('product_name'), Vendor= inventory_record.get('vendor'), MRP=int(inventory_record.get('mrp')),
                                                    batch_num=int(inventory_record.get('batch_num')), batch_date=inventory_record.get('batch_date'), Quantity=int(inventory_record.get('quantity')), status='APPROVED', inventory= inventory_object)

                inventory_record.save()
                response.append({'success': True})
            else:
                status = HTTP_200_OK
                add_permission = InventoryPermissions(inventory_name=inventory_name, permission_codename='can_add_record_to_%s'%inventory_name, target_user=user.username, store_manager=inventory_object.store_manager)
                add_permission.save()

                response.append({'success': 'your permission to add record to this inventory is pending approval'})

        except Exception as e:
            status = HTTP_400_BAD_REQUEST
            response.append({'error': 'Error occured in processing request'})

        return HttpResponse(json.dumps(response), status=status, content_type='application/json')

    def put(self, request):
        user = request.user
        inventory_user = InventoryUser.user_exists(username=user.username)
        request_data = json.loads(request.body)
        inventory_name = request_data.get('inventory_name')
        updated_data = request_data.get('updated_data')
        status = HTTP_200_OK
        response = []
        try:
            inventory_object = Inventory.objects.filter(inventory_name=inventory_name).first()

            if inventory_object.user_can_edit_record_of_inventory(inventory_user):
                inventory_record = InventoryRecords.objects.get(product_name=updated_data.get('product_name'))
                if inventory_record:
                    inventory_record.product_id = int(updated_data.get('product_id'))
                    inventory_record.Vendor = updated_data.get('vendor')
                    inventory_record.MRP = int(updated_data.get('mrp'))
                    inventory_record.batch_num = int(updated_data.get('batch_num'))
                    inventory_record.batch_date = updated_data.get('batch_date')
                    inventory_record.Quantity = int(updated_data.get('quantity'))
                    inventory_record.save()

                    response.append({'success': True})
            else:
                status = HTTP_200_OK
                add_permission = InventoryPermissions(inventory_name=inventory_name,
                                                      permission_codename='can_edit_record_of_%s' % inventory_name,
target_user=user.username, store_manager=inventory_object.store_manager)
                add_permission.save()

                response.append({'success': 'your permission to edit record of this inventory is pending approval'})

        except Exception as e:
            status = HTTP_400_BAD_REQUEST
            response.append({'error': 'Error occured in processing request'})

        return HttpResponse(json.dumps(response), status=status, content_type='application/json')

    def delete(self, request):
        user = request.user
        inventory_user = InventoryUser.user_exists(username=user.username)
        inventory_name = request.GET.get('inventory_name')
        inventory_record_name = request.GET.get('product_name')
        status = HTTP_200_OK
        response = []
        try:
            inventory_object = Inventory.objects.filter(inventory_name=inventory_name).first()

            if inventory_object.user_can_delete_record_from_inventory(inventory_user):
                inventory_record = InventoryRecords.objects.get(product_name=inventory_record_name)
                if inventory_record:
                    inventory_record.delete()
                    response.append({'success': True})
            else:
                status = HTTP_200_OK
                add_permission = InventoryPermissions(inventory_name=inventory_name, permission_codename='can_delete_record_from_%s' % inventory_name, target_user=user.username, store_manager=inventory_object.store_manager)
                add_permission.save()

                response.append({'success': 'your permission to delete record from this inventory is pending approval'})

        except Exception as e:
            status = HTTP_400_BAD_REQUEST
            response.append({'error': 'Error occured in processing request'})

        return HttpResponse(json.dumps(response), status=status, content_type='application/json')












