from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('profileauth/', include('profileauth.urls', namespace='profileauth')),
    path('profileauth/accounts/', include('allauth.urls')),
    path('social/', include('social.urls', namespace='social')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
