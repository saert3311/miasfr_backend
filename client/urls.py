from django.urls import path

from . import views

urlpatterns = [
    path('clients/', views.client_list_view),
    path('clients/anon/', views.anon_client_create_view),
    path('clients/search', views.single_client_view),
    path('clients/create/', views.client_create_view),
    path('clients/<int:pk>/', views.client_retrieve_view),
    path('address/create/', views.address_create_view),
    path('calls/', views.call_create_list_view)
]