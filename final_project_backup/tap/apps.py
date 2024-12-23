from django.apps import AppConfig

class TapConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "tap"

    def ready(self):
        self.add_user_groups()

    def add_user_groups(self):
        from django.contrib.auth.models import Group
        groups = ["농가", "일반 회원"]
        for group_name in groups:
            Group.objects.get_or_create(name=group_name)
