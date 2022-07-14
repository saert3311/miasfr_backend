from django.urls import path

from .views import root_redirect

app_name = 'common'

urlpatterns = [
    path('', root_redirect),
]