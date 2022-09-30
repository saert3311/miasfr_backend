from django.urls import path

from . import views

app_name = 'inventory'

urlpatterns = [
    path('inventory/category/', views.category_view),
    path('inventory/periods/', views.period_list_view),
    path('inventory/item/', views.item_list_view),
    path('inventory/item/<int:pk>/', views.item_retrieve_view),
    path('inventory/item/<int:pk>/prices/', views.item_prices_view),
    path('inventory/item/create/', views.item_create_view)
]