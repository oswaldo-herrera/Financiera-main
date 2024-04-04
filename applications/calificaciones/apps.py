from django.apps import AppConfig


class CalifiacacionesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'applications.calificaciones'

    
    def ready(self):
        import applications.calificaciones.signals