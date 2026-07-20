from django.apps import AppConfig

class BtlConfig(AppConfig): # Tên class này nên là BtlConfig
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'btl' # Phải khớp với tên thư mục