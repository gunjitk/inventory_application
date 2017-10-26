# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.views.generic import TemplateView
from rest_framework.authentication import TokenAuthentication
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_403_FORBIDDEN
from rest_framework.views import APIView
from django.shortcuts import render_to_response
import json

from inventory_application import settings
from inventory_manager.models import InventoryUser


class RegisterUser(APIView):

    def post(self, request):

        user_data = json.loads(request.body)

        username = user_data.get('user_name')
        password = user_data.get('password')
        role = user_data.get('user_role')
        email = user_data.get('user_email')

        role = role.split('|')

        if not InventoryUser.user_exists(username=username):

            user = User.objects.create_user(username, email, password)
            InventoryUser.objects.create(user=user, name=username, is_dept_mgr = True if "DEPT_MGR" in role else False, is_store_mgr = True if "STORE_MGR" in role else False)

            return HttpResponse(json.dumps({"success": True}), content_type="application/json", status=HTTP_200_OK)

        else:
            raise ValidationError("Member already exists. Continue to login!!!")


class UpdateUserSpecificDetails(APIView):
    authentication_classes = (TokenAuthentication,)

    def put(self, request):

        user = request.user
        user_data = json.loads(request.body)
        status = HTTP_200_OK
        error = ""

        try:
            InventoryUser.update_user_data(user_data, user.id)
        except Exception as e:
            status = HTTP_400_BAD_REQUEST
            error = "Failed to update user details"

        return HttpResponse(json.dumps({"error":error}), content_type="application/json", status=status)




