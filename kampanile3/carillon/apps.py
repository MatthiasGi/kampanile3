from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CarillonConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "carillon"
    verbose_name = _("Carillon")

    def ready(self):
        from .lib import init_schedule

        init_schedule()
