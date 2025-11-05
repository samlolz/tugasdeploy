"""
FITURBERITA/models.py
Model untuk BERITA dan Komentar
"""

from django.db import models


class BERITA(models.Model):
    """
    Model untuk menyimpan data BERITA
    """
    judul = models.CharField(max_length=200, verbose_name="Judul BERITA")
    tanggal = models.DateTimeField(auto_now_add=True, verbose_name="Tanggal Publish")
    isi_BERITA = models.TextField(verbose_name="Isi BERITA")
    gambar = models.ImageField(
        upload_to='BERITA_images/', 
        blank=True, 
        null=True,
        verbose_name="Gambar BERITA"
    )
    
    class Meta:
        verbose_name = "BERITA"
        verbose_name_plural = "BERITA"
        ordering = ['-tanggal']  # Urutkan dari yang terbaru
    
    def __str__(self):
        return self.judul
    
    def get_jumlah_komentar(self):
        """Method untuk menghitung jumlah komentar"""
        return self.komentar.count()


class Komentar(models.Model):
    """
    Model untuk menyimpan komentar pada BERITA
    """
    nama = models.CharField(max_length=100, verbose_name="Nama Pemberi Komentar")
    tanggal = models.DateTimeField(auto_now_add=True, verbose_name="Tanggal Komentar")
    isi_komentar = models.TextField(verbose_name="Isi Komentar")
    BERITA = models.ForeignKey(
        BERITA, 
        on_delete=models.CASCADE, 
        related_name='komentar',
        verbose_name="BERITA"
    )
    
    class Meta:
        verbose_name = "Komentar"
        verbose_name_plural = "Komentar"
        ordering = ['-tanggal']  # Urutkan dari yang terbaru
    
    def __str__(self):
        return f"Komentar oleh {self.nama} pada {self.BERITA.judul}"