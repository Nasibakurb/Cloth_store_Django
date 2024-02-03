from django.apps import AppConfig


class ClothshopConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ClothShop'

    def ready(self):
        import ClothShop.signals
