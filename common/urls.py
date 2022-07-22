from django.urls import path

from .views import *

app_name = 'common'

urlpatterns = [
    path('', root_redirect),
    path('api/v1/userdetail/<int:pk>', user_detail_view)
]