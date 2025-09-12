from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .forms import InputForm
from .models import Input


class InputListView(LoginRequiredMixin, ListView):
    model = Input

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "menu_active": "input",
                "title": _("Inputs"),
                "subtitle": _("The following inputs are configured for this board:"),
            }
        )
        return context


class InputDetailView(LoginRequiredMixin, DetailView):
    model = Input

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "menu_active": "input",
                "back_link": reverse("gpio:inputs:list"),
                "title": _("Input: %(name)s") % {"name": self.object.name},
            }
        )
        return context


class InputCreateView(LoginRequiredMixin, CreateView):
    model = Input
    form_class = InputForm
    template_name = "frontend/simple_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "menu_active": "input",
                "back_link": reverse("gpio:inputs:list"),
                "title": _("Create input"),
                "subtitle": _("Add a GPIO input to trigger a striker."),
            }
        )
        return context


class InputUpdateView(LoginRequiredMixin, UpdateView):
    model = Input
    form_class = InputForm
    template_name = "frontend/simple_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "menu_active": "input",
                "back_link": self.object.get_absolute_url(),
                "title": _("Update GPIO input"),
                "subtitle": self.object.name,
            }
        )
        return context


class InputDeleteView(LoginRequiredMixin, DeleteView):
    model = Input
    template_name = "frontend/confirm_delete.html"

    def get_success_url(self):
        return reverse("gpio:inputs:list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "menu_active": "input",
                "back_link": reverse("gpio:inputs:list"),
                "title": _("Delete GPIO input"),
                "subtitle": _(
                    'Are you sure you want to delete the GPIO input "%(name)s"?'
                )
                % {"name": self.object.name},
            }
        )
        return context
