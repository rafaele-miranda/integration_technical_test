# workorders/apps.py
from django.apps import AppConfig

class WorkordersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'workorders'

    def ready(self):
        import workorders.signals