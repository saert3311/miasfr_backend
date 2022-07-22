from django.urls import path

from client import views

urlpatterns = [
    path('clients/all/', views.AllClientsList.as_view()),
    path('clients/<int:pk>/', views.client_detail_view)
]