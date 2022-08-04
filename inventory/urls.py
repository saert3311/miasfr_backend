from django.urls import path

from . import views

app_name = 'inventory'

urlpatterns = [
    path('inventory/category/', views.category_view),
    path('inventory/item/create/', views.item_create_view)
]