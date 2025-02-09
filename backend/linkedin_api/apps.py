from django.apps import AppConfig
    

class LinkedinApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'linkedin_api'
    verbose_name = 'LinkedIn API'

    def ready(self):
        import linkedin_api.signals  # noqa: F401 