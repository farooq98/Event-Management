from django.apps import AppConfig


class MigrationTestConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'migration_test'
