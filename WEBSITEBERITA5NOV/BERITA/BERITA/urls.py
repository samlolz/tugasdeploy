"""
BERITA/urls.py
Main URL routing untuk project BERITA
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Schema view untuk Swagger documentation (optional)
schema_view = get_schema_view(
    openapi.Info(
        title="BERITA API",
        default_version='v1',
        description="API Documentation untuk Website BERITA",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@BERITA.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Admin panel
    path('admin/', admin.site.urls),
    
    # API endpoints
    path('api/', include('FITURBERITA.urls')),
    
    # API documentation (optional - butuh install drf-yasg)
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    # DRF browsable API authentication
    path('api-auth/', include('rest_framework.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

