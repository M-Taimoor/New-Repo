from django.apps import AppConfig


class TasksConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tasks'



# your_app/apps.py
from django.apps import AppConfig

class YourAppConfig(AppConfig):
    name = 'drf_spectacular'  # Rename from 'staticfiles' to 'your_app'
    verbose_name = 'tasks'