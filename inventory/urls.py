from django.conf.urls import url, include
from django.contrib import admin

from inventory import views

urlpatterns = [
    url(r'^list/', views.InventoryView.as_view()),
    url(r'^show_all_pending_approvals/', views.InventoryPermissionView.as_view()),
    url(r'^add_item_to_inventory/', views.InventoryUpdateView.as_view()),
    url(r'^approve_permission/', views.InventoryPermissionView.as_view()),
    url(r'^delete_record/', views.InventoryUpdateView.as_view()),
    url(r'^subscribe/', views.InventoryView.as_view())
]