from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from ..forms import RuleForm, StrikerForm
from ..models import Rule, Striker


class StrikerListView(LoginRequiredMixin, ListView):
    model = Striker

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "title": _("Strikers"),
                "subtitle": _("The following strikers are configured in the system:"),
            }
        )
        return context


class StrikerDetailView(LoginRequiredMixin, DetailView):
    model = Striker

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "back_link": reverse("carillon:strikers:list"),
                "title": self.object.name,
                "rule_list": self.object.rules.all(),
            }
        )
        return context


class StrikerCreateView(LoginRequiredMixin, CreateView):
    model = Striker
    form_class = StrikerForm
    template_name = "frontend/simple_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "back_link": reverse("carillon:strikers:list"),
                "title": _("Create striker"),
                "subtitle": _("Add a striker as a container for rules."),
            }
        )
        return context


class StrikerUpdateView(LoginRequiredMixin, UpdateView):
    model = Striker
    form_class = StrikerForm
    template_name = "frontend/simple_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "back_link": self.object.get_absolute_url(),
                "title": _("Update striker"),
                "subtitle": self.object.name,
            }
        )
        return context


class StrikerDeleteView(LoginRequiredMixin, DeleteView):
    model = Striker
    template_name = "frontend/confirm_delete.html"
    success_url = reverse_lazy("carillon:strikers:list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "back_link": reverse("carillon:strikers:list"),
                "title": _("Delete striker"),
                "subtitle": _(
                    'Are you sure you want to delete the striker "%(name)s"?'
                    % {"name": self.object.name}
                ),
            }
        )
        return context


class StrikerRuleDetailView(LoginRequiredMixin, DetailView):
    model = Rule

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "back_link": self.object.striker.get_absolute_url(),
                "title": self.object.name,
            }
        )
        return context


class StrikerRuleCreateView(LoginRequiredMixin, CreateView):
    model = Rule
    form_class = RuleForm
    template_name = "frontend/simple_form.html"

    @property
    def _striker(self):
        return Striker.objects.get(pk=self.kwargs.get("pk"))

    def get_initial(self):
        initial = super().get_initial()
        initial["striker"] = self._striker
        return initial

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["striker"] = self._striker
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        striker = Striker.objects.get(pk=self.kwargs.get("pk"))
        context.update(
            {
                "back_link": striker.get_absolute_url(),
                "title": _("Create rule"),
                "subtitle": _(
                    'Add a rule for automatically playing songs on striker "%(name)s".'
                )
                % {"name": striker.name},
            }
        )
        return context


class StrikerRuleUpdateView(LoginRequiredMixin, UpdateView):
    model = Rule
    form_class = RuleForm
    template_name = "frontend/simple_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "back_link": self.object.get_absolute_url(),
                "title": _("Update a rule"),
                "subtitle": self.object.name,
            }
        )
        return context


class StrikerRuleDeleteView(LoginRequiredMixin, DeleteView):
    model = Rule
    template_name = "frontend/confirm_delete.html"

    def get_success_url(self):
        return self.object.striker.get_absolute_url()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "back_link": self.object.striker.get_absolute_url(),
                "title": _("Delete rule"),
                "subtitle": _('Are you sure you want to delete the rule "%(name)s"?')
                % {"name": self.object.name},
            }
        )
        return context
