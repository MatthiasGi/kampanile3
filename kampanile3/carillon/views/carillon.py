import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext as _
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from ..forms import CarillonForm
from ..models import Carillon


class CarillonListView(LoginRequiredMixin, ListView):
    model = Carillon

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "menu_active": "carillon",
                "title": _("Carillons"),
                "subtitle": _("The following carillons are configured in the system:"),
            }
        )
        return context


class CarillonDetailView(LoginRequiredMixin, DetailView):
    model = Carillon

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "menu_active": "carillon",
                "back_link": reverse("carillon:carillons:list"),
                "title": _("Carillon: %(name)s") % {"name": self.object.name},
            }
        )
        return context


class CarillonCreateView(LoginRequiredMixin, CreateView):
    model = Carillon
    form_class = CarillonForm
    template_name = "carillon/simple_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "menu_active": "carillon",
                "back_link": reverse("carillon:carillons:list"),
                "title": _("Create carillon"),
                "subtitle": _("Add a carillon to play notes on."),
            }
        )
        return context


class CarillonUpdateView(LoginRequiredMixin, UpdateView):
    model = Carillon
    form_class = CarillonForm
    template_name = "carillon/simple_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "menu_active": "carillon",
                "back_link": self.object.get_absolute_url(),
                "title": _("Modify carillon"),
                "subtitle": _("Modify the settings of the carillon: %(name)s")
                % {"name": self.object.name},
            }
        )
        return context


class CarillonDeleteView(LoginRequiredMixin, DeleteView):
    model = Carillon
    template_name = "carillon/confirm_delete.html"
    success_url = reverse_lazy("carillon:carillons:list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "menu_active": "carillon",
                "back_link": reverse("carillon:carillons:list"),
                "title": _("Delete carillon"),
                "subtitle": _("Are you sure you want to delete carillon %(name)s?")
                % {"name": self.object.name},
            }
        )
        return context


@login_required
@csrf_exempt
def hit_note_view(request, pk):
    """Simple view to hit a note on a specific carillon."""
    if request.method != "POST":
        return JsonResponse({"error": "Only POST method allowed"}, status=405)

    try:
        carillon = get_object_or_404(Carillon, pk=pk)
        note = int(json.loads(request.body).get("note"))
        if note is None:
            return JsonResponse({"error": "Note parameter is required"}, status=400)
        if not (0 <= note <= 127):
            return JsonResponse({"error": "Note must be between 0 and 127"}, status=400)
        carillon.hit(note)
        return JsonResponse({"success": True, "carillon_id": pk, "note": note})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@login_required
@csrf_exempt
def stop_view(request, pk):
    """Simple view to stop the current song on a specific carillon."""
    if request.method != "POST":
        return JsonResponse({"error": "Only POST method allowed"}, status=405)

    try:
        carillon = get_object_or_404(Carillon, pk=pk)
        carillon.stop()
        return JsonResponse({"success": True, "carillon_id": pk})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
