"""
FITURBERITA/views.py
Views untuk API BERITA dan Komentar menggunakan ViewSet
"""

from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import BERITA, Komentar
from .serializers import (
    BERITASerializer, 
    BERITAListSerializer, 
    KomentarSerializer,
    KomentarCreateSerializer
)


class BERITAViewSet(viewsets.ModelViewSet):
    """
    ViewSet untuk CRUD BERITA
    
    Endpoints:
    - GET /api/BERITA/ : List semua BERITA
    - POST /api/BERITA/ : Buat BERITA baru
    - GET /api/BERITA/{id}/ : Detail BERITA
    - PUT /api/BERITA/{id}/ : Update BERITA
    - PATCH /api/BERITA/{id}/ : Partial update BERITA
    - DELETE /api/BERITA/{id}/ : Hapus BERITA
    - GET /api/BERITA/{id}/komentar/ : List komentar untuk BERITA tertentu
    """
    queryset = BERITA.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['judul', 'isi_BERITA']  # Field yang bisa di-search
    ordering_fields = ['tanggal', 'judul']  # Field yang bisa di-order
    ordering = ['-tanggal']  # Default ordering
    
    def get_serializer_class(self):
        """
        Gunakan serializer berbeda untuk list dan detail
        List: tanpa nested komentar (lebih ringan)
        Detail: dengan nested komentar (lebih lengkap)
        """
        if self.action == 'list':
            return BERITAListSerializer
        return BERITASerializer
    
    def create(self, request, *args, **kwargs):
        """Override create untuk custom response"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {
                'message': 'BERITA berhasil dibuat',
                'data': serializer.data
            },
            status=status.HTTP_201_CREATED,
            headers=headers
        )
    
    def update(self, request, *args, **kwargs):
        """Override update untuk custom response"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({
            'message': 'BERITA berhasil diupdate',
            'data': serializer.data
        })
    
    def destroy(self, request, *args, **kwargs):
        """Override destroy untuk custom response"""
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {'message': 'BERITA berhasil dihapus'},
            status=status.HTTP_200_OK
        )
    
    @action(detail=True, methods=['get'])
    def komentar(self, request, pk=None):
        """
        Custom action untuk mendapatkan semua komentar dari BERITA tertentu
        Endpoint: GET /api/BERITA/{id}/komentar/
        """
        BERITA = self.get_object()
        komentar = BERITA.komentar.all()
        serializer = KomentarSerializer(komentar, many=True)
        return Response({
            'BERITA': BERITA.judul,
            'jumlah_komentar': komentar.count(),
            'komentar': serializer.data
        })
    
    @action(detail=False, methods=['get'])
    def terbaru(self, request):
        """
        Custom action untuk mendapatkan 5 BERITA terbaru
        Endpoint: GET /api/BERITA/terbaru/
        """
        BERITA_terbaru = self.queryset[:5]
        serializer = self.get_serializer(BERITA_terbaru, many=True)
        return Response(serializer.data)


class KomentarViewSet(viewsets.ModelViewSet):
    """
    ViewSet untuk CRUD Komentar
    
    Endpoints:
    - GET /api/komentar/ : List semua komentar
    - POST /api/komentar/ : Buat komentar baru
    - GET /api/komentar/{id}/ : Detail komentar
    - PUT /api/komentar/{id}/ : Update komentar
    - PATCH /api/komentar/{id}/ : Partial update komentar
    - DELETE /api/komentar/{id}/ : Hapus komentar
    """
    queryset = Komentar.objects.all()
    serializer_class = KomentarSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['BERITA', 'nama']  # Field yang bisa di-filter
    ordering_fields = ['tanggal']  # Field yang bisa di-order
    ordering = ['-tanggal']  # Default ordering
    
    def get_serializer_class(self):
        """Gunakan serializer berbeda untuk create"""
        if self.action == 'create':
            return KomentarCreateSerializer
        return KomentarSerializer
    
    def create(self, request, *args, **kwargs):
        """Override create untuk custom response"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {
                'message': 'Komentar berhasil ditambahkan',
                'data': serializer.data
            },
            status=status.HTTP_201_CREATED,
            headers=headers
        )
    
    def update(self, request, *args, **kwargs):
        """Override update untuk custom response"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({
            'message': 'Komentar berhasil diupdate',
            'data': serializer.data
        })
    
    def destroy(self, request, *args, **kwargs):
        """Override destroy untuk custom response"""
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {'message': 'Komentar berhasil dihapus'},
            status=status.HTTP_200_OK
        )