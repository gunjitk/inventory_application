from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from rest_framework.authtoken import views as django_view

from inventory_manager import views

urlpatterns = [
        url(r'^register_user/', views.RegisterUser.as_view()),
        url(r'^login/', django_view.obtain_auth_token),
        url(r'^update_user_details/', views.UpdateUserSpecificDetails.as_view())
    ]