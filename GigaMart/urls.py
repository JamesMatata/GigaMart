from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf import settings

admin.site.site_title = 'GigaMart | Admin'
admin.site.site_header = 'GigaMart | Admin'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('store.urls', namespace='store')),
    path('basket/', include('basket.urls', namespace='basket')),
    path('accounts/', include('accounts.urls', namespace='accounts')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
