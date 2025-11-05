"""
FITURBERITA/serializers.py
Serializers untuk API BERITA dan Komentar
"""

from rest_framework import serializers
from .models import BERITA, Komentar


class KomentarSerializer(serializers.ModelSerializer):
    """
    Serializer untuk model Komentar
    Digunakan untuk membuat, update, dan menampilkan komentar
    """
    class Meta:
        model = Komentar
        fields = ['id', 'nama', 'tanggal', 'isi_komentar', 'BERITA']
        read_only_fields = ['tanggal']  # Tanggal otomatis terisi
    
    def validate_isi_komentar(self, value):
        """Validasi agar komentar tidak kosong"""
        if not value.strip():
            raise serializers.ValidationError("Isi komentar tidak boleh kosong")
        return value


class BERITASerializer(serializers.ModelSerializer):
    """
    Serializer lengkap untuk model BERITA
    Include nested komentar dan jumlah komentar
    Digunakan untuk detail view
    """
    komentar = KomentarSerializer(many=True, read_only=True)
    jumlah_komentar = serializers.SerializerMethodField()
    
    class Meta:
        model = BERITA
        fields = [
            'id', 
            'judul', 
            'tanggal', 
            'isi_BERITA', 
            'gambar', 
            'komentar', 
            'jumlah_komentar'
        ]
        read_only_fields = ['tanggal']
    
    def get_jumlah_komentar(self, obj):
        """Method untuk menghitung jumlah komentar"""
        return obj.komentar.count()
    
    def validate_judul(self, value):
        """Validasi agar judul tidak kosong"""
        if not value.strip():
            raise serializers.ValidationError("Judul tidak boleh kosong")
        return value
    
    def validate_isi_BERITA(self, value):
        """Validasi agar isi BERITA tidak kosong"""
        if not value.strip():
            raise serializers.ValidationError("Isi BERITA tidak boleh kosong")
        return value


class BERITAListSerializer(serializers.ModelSerializer):
    """
    Serializer ringkas untuk model BERITA
    Tanpa nested komentar untuk performa lebih baik di list view
    """
    jumlah_komentar = serializers.SerializerMethodField()
    
    class Meta:
        model = BERITA
        fields = [
            'id', 
            'judul', 
            'tanggal', 
            'isi_BERITA', 
            'gambar', 
            'jumlah_komentar'
        ]
        read_only_fields = ['tanggal']
    
    def get_jumlah_komentar(self, obj):
        """Method untuk menghitung jumlah komentar"""
        return obj.komentar.count()


class KomentarCreateSerializer(serializers.ModelSerializer):
    """
    Serializer khusus untuk membuat komentar baru
    dengan informasi BERITA yang lebih lengkap
    """
    BERITA_judul = serializers.CharField(source='BERITA.judul', read_only=True)
    
    class Meta:
        model = Komentar
        fields = ['id', 'nama', 'tanggal', 'isi_komentar', 'BERITA', 'BERITA_judul']
        read_only_fields = ['tanggal', 'BERITA_judul']