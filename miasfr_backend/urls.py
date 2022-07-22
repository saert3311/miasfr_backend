from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

BASE_API_ENDPOINT = 'api/v1/'

urlpatterns = [
    path('admin/', admin.site.urls),
    path(BASE_API_ENDPOINT, include('djoser.urls')),
    path(BASE_API_ENDPOINT, include('djoser.urls.authtoken')),
    path(BASE_API_ENDPOINT, include('client.urls')),
    path('', include('common.urls', namespace='common'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
