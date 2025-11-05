"""
FITURBERITA/urls.py
URL routing untuk app FITURBERITA (REST API)
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BERITAViewSet, KomentarViewSet

# namespace app (opsional)
app_name = "FITURBERITA"

# router otomatis
router = DefaultRouter()
router.register(r'BERITA', BERITAViewSet, basename='BERITA')
router.register(r'komentar', KomentarViewSet, basename='komentar')

urlpatterns = [
    path('', include(router.urls)),
    # auth endpoint opsional (browsable API login/logout)
    path('auth/', include('rest_framework.urls', namespace='rest_framework')),
]
