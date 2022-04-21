from django.urls import path, include

from client import views

urlpatterns = [
    path('all-clients/', views.AllClientsList.as_view()),
]