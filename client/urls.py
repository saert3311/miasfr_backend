from django.urls import path

from . import views

urlpatterns = [
    path('clients/', views.client_list_view),
    path('clients/anon/', views.anon_client_create_view),
    path('clients/search', views.single_client_view),
    path('clients/create/', views.client_create_view),
    path('clients/create/<int:pk>/', views.client_create_view),
    path('clients/<int:pk>/', views.client_retrieve_view),
    path('address/create/', views.address_create_view),
    path('calls/', views.call_create_list_view),
    path('calls/all/', views.all_calls_view),
    path('calls/latest/', views.last_call_info_view),
    path('calls/resume/', views.resume_calls_view),
    path('msj/', views.sent_messages_view),
    path('msj/balance/', views.check_balance),
    path('msj/send/', views.send_sms_view),
]