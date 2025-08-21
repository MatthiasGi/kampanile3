from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from ..forms import RuleForm
from ..models import Rule


class RuleListView(LoginRequiredMixin, ListView):
    model = Rule

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "menu_active": "rule",
                "title": _("Rules"),
                "subtitle": _("The following rules are configured in the system:"),
            }
        )
        return context


class RuleDetailView(LoginRequiredMixin, DetailView):
    model = Rule

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "menu_active": "rule",
                "back_link": reverse("carillon:rules:list"),
                "title": self.object.name,
            }
        )
        return context


class RuleCreateView(LoginRequiredMixin, CreateView):
    model = Rule
    form_class = RuleForm
    template_name = "carillon/simple_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "menu_active": "rule",
                "back_link": reverse("carillon:rules:list"),
                "title": _("Create rule"),
                "subtitle": _("Add a rule for automatically playing songs."),
            }
        )
        return context


class RuleUpdateView(LoginRequiredMixin, UpdateView):
    model = Rule
    form_class = RuleForm
    template_name = "carillon/simple_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "menu_active": "rule",
                "back_link": self.object.get_absolute_url(),
                "title": _("Update a rule"),
                "subtitle": self.object.name,
            }
        )
        return context


class RuleDeleteView(LoginRequiredMixin, DeleteView):
    model = Rule
    template_name = "carillon/confirm_delete.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "menu_active": "rule",
                "back_link": reverse("carillon:rules:list"),
                "title": _("Delete rule"),
                "subtitle": _('Are you sure you want to delete the rule "%(name)s"?')
                % {"name": self.object.name},
            }
        )
        return context
