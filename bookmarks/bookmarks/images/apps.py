from django.apps import AppConfig


class ImagesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'images'

    def ready(self):
        # Импортируем файл с описанной функцией-подписчиком на сигнал.
        import images.signals