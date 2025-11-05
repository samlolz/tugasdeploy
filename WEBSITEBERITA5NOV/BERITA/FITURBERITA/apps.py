from django.apps import AppConfig


class FITURBERITAConfig(AppConfig):
    """
    Configuration class untuk FITURBERITA app
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'FITURBERITA'
    verbose_name = 'Fitur BERITA'
    
    def ready(self):
        """
        Method yang dipanggil ketika Django starts
        Bisa digunakan untuk register signals, dll
        """
        # Import signals here if needed
        # import FITURBERITA.signals
        pass