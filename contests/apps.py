from django.apps import AppConfig

# configure some of the attributes of the application.
class ContestsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'contests'
