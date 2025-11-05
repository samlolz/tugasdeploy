"""
FITURBERITA/admin.py
Django Admin configuration untuk BERITA dan Komentar
"""

from django.contrib import admin
from django.utils.html import format_html
from .models import BERITA, Komentar


@admin.register(BERITA)
class BERITAAdmin(admin.ModelAdmin):
    """
    Admin configuration untuk model BERITA
    """
    # Fields yang ditampilkan di list view
    list_display = [
        'id',
        'judul',
        'preview_gambar',
        'tanggal',
        'get_jumlah_komentar',
        'preview_isi'
    ]
    
    # Fields yang bisa diklik untuk ke detail
    list_display_links = ['id', 'judul']
    
    # Filter di sidebar
    list_filter = ['tanggal']
    
    # Search fields
    search_fields = ['judul', 'isi_BERITA']
    
    # Readonly fields
    readonly_fields = ['tanggal', 'preview_gambar_besar']
    
    # Fields grouping di form
    fieldsets = (
        ('Informasi BERITA', {
            'fields': ('judul', 'isi_BERITA')
        }),
        ('Media', {
            'fields': ('gambar', 'preview_gambar_besar')
        }),
        ('Informasi Waktu', {
            'fields': ('tanggal',),
            'classes': ('collapse',)
        }),
    )
    
    # Pagination
    list_per_page = 20
    
    # Ordering
    ordering = ['-tanggal']
    
    # Date hierarchy
    date_hierarchy = 'tanggal'
    
    def get_jumlah_komentar(self, obj):
        """
        Custom column untuk menampilkan jumlah komentar
        """
        count = obj.komentar.count()
        if count > 0:
            return format_html(
                '<span style="background-color: #4CAF50; color: white; padding: 3px 10px; border-radius: 3px;">{}</span>',
                count
            )
        return format_html(
            '<span style="background-color: #f44336; color: white; padding: 3px 10px; border-radius: 3px;">0</span>'
        )
    get_jumlah_komentar.short_description = 'Jumlah Komentar'
    
    def preview_isi(self, obj):
        """
        Menampilkan preview isi BERITA (100 karakter pertama)
        """
        if len(obj.isi_BERITA) > 100:
            return obj.isi_BERITA[:100] + '...'
        return obj.isi_BERITA
    preview_isi.short_description = 'Preview Isi BERITA'
    
    def preview_gambar(self, obj):
        """
        Menampilkan thumbnail gambar di list view
        """
        if obj.gambar:
            return format_html(
                '<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 5px;" />',
                obj.gambar.url
            )
        return format_html('<span style="color: #999;">Tidak ada gambar</span>')
    preview_gambar.short_description = 'Gambar'
    
    def preview_gambar_besar(self, obj):
        """
        Menampilkan gambar yang lebih besar di form view
        """
        if obj.gambar:
            return format_html(
                '<img src="{}" width="300" style="border-radius: 5px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);" />',
                obj.gambar.url
            )
        return format_html('<span style="color: #999;">Tidak ada gambar</span>')
    preview_gambar_besar.short_description = 'Preview Gambar'
    
    def save_model(self, request, obj, form, change):
        """
        Override save_model untuk menambahkan custom logic
        """
        super().save_model(request, obj, form, change)
        if not change:  # Jika create baru
            self.message_user(request, f'BERITA "{obj.judul}" berhasil dibuat!')
        else:  # Jika update
            self.message_user(request, f'BERITA "{obj.judul}" berhasil diupdate!')


@admin.register(Komentar)
class KomentarAdmin(admin.ModelAdmin):
    """
    Admin configuration untuk model Komentar
    """
    # Fields yang ditampilkan di list view
    list_display = [
        'id',
        'nama',
        'get_BERITA_judul',
        'preview_komentar',
        'tanggal',
        'status_komentar'
    ]
    
    # Fields yang bisa diklik untuk ke detail
    list_display_links = ['id', 'nama']
    
    # Filter di sidebar
    list_filter = ['tanggal', 'BERITA']
    
    # Search fields
    search_fields = ['nama', 'isi_komentar', 'BERITA__judul']
    
    # Readonly fields
    readonly_fields = ['tanggal']
    
    # Fields grouping di form
    fieldsets = (
        ('Informasi Pemberi Komentar', {
            'fields': ('nama',)
        }),
        ('Komentar', {
            'fields': ('BERITA', 'isi_komentar')
        }),
        ('Informasi Waktu', {
            'fields': ('tanggal',),
            'classes': ('collapse',)
        }),
    )
    
    # Pagination
    list_per_page = 20
    
    # Ordering
    ordering = ['-tanggal']
    
    # Date hierarchy
    date_hierarchy = 'tanggal'
    
    # Autocomplete fields (untuk foreign key)
    autocomplete_fields = ['BERITA']
    
    def get_BERITA_judul(self, obj):
        """
        Menampilkan judul BERITA dengan link
        """
        return format_html(
            '<a href="/admin/FITURBERITA/BERITA/{}/change/" style="color: #0066cc;">{}</a>',
            obj.BERITA.id,
            obj.BERITA.judul
        )
    get_BERITA_judul.short_description = 'BERITA'
    
    def preview_komentar(self, obj):
        """
        Menampilkan preview komentar (80 karakter pertama)
        """
        if len(obj.isi_komentar) > 80:
            return obj.isi_komentar[:80] + '...'
        return obj.isi_komentar
    preview_komentar.short_description = 'Isi Komentar'
    
    def status_komentar(self, obj):
        """
        Menampilkan status badge untuk komentar
        """
        return format_html(
            '<span style="background-color: #2196F3; color: white; padding: 3px 10px; border-radius: 3px;">Aktif</span>'
        )
    status_komentar.short_description = 'Status'
    
    def save_model(self, request, obj, form, change):
        """
        Override save_model untuk menambahkan custom logic
        """
        super().save_model(request, obj, form, change)
        if not change:  # Jika create baru
            self.message_user(request, f'Komentar dari "{obj.nama}" berhasil ditambahkan!')
        else:  # Jika update
            self.message_user(request, f'Komentar dari "{obj.nama}" berhasil diupdate!')


# Customize admin site headers
admin.site.site_header = "BERITA - Admin Panel"
admin.site.site_title = "BERITA Admin"
admin.site.index_title = "Selamat Datang di BERITA Admin Panel"