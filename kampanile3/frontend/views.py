from carillon.models import Carillon, Rule, Song, Striker
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext as _
from django.views.generic import TemplateView


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "frontend/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "title": _("Overview"),
                "subtitle": _("Welcome to your carillon management interface!"),
                "carillons": Carillon.objects.all(),
                "sample_songs": Song.objects.order_by("-id")[:4],
                "num_songs": Song.objects.count(),
                "num_rules": Rule.objects.count(),
                "num_strikers": Striker.objects.count(),
                "default_carillon": Carillon.get_default(),
            }
        )
        return context
