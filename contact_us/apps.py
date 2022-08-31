from django.apps import AppConfig

# configure some of the attributes of the application.
class ContactUsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'contact_us'
