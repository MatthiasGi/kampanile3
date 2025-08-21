import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from ..forms import SongForm
from ..models import Carillon, Song


class SongListView(LoginRequiredMixin, ListView):
    model = Song

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "menu_active": "song",
                "title": _("Songs"),
                "subtitle": _(
                    "The following songs are available in the carillon to play:"
                ),
            }
        )
        return context


class SongDetailView(LoginRequiredMixin, DetailView):
    model = Song

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "menu_active": "song",
                "back_link": reverse("carillon:songs:list"),
                "title": self.object.name,
                "carillons": Carillon.objects.all(),
            }
        )
        return context


class SongCreateView(LoginRequiredMixin, CreateView):
    model = Song
    form_class = SongForm
    template_name = "carillon/simple_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "menu_active": "song",
                "back_link": reverse("carillon:songs:list"),
                "title": _("Create song"),
                "subtitle": _("Add a song to the carillon."),
            }
        )
        return context


class SongUpdateView(LoginRequiredMixin, UpdateView):
    model = Song
    form_class = SongForm
    template_name = "carillon/simple_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "menu_active": "song",
                "back_link": self.object.get_absolute_url(),
                "title": _("Update song"),
                "subtitle": self.object.name,
            }
        )
        return context


class SongDeleteView(LoginRequiredMixin, DeleteView):
    model = Song
    template_name = "carillon/confirm_delete.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "menu_active": "song",
                "back_link": reverse("carillon:songs:list"),
                "title": _("Delete song"),
                "subtitle": _("Are you sure you want to delete the song: %(name)s?")
                % {"name": self.object.name},
            }
        )
        return context


@login_required
@csrf_exempt
def play_view(request, pk):
    """Simple view to play a song on a specific carillon."""
    if request.method != "POST":
        return JsonResponse({"error": "Only POST method allowed"}, status=405)

    try:
        song = get_object_or_404(Song, pk=pk)
        data = json.loads(request.body)
        carillon = get_object_or_404(Carillon, pk=data.get("carillon_id"))
        return JsonResponse(
            {"success": carillon.play(song.midi), "carillon_id": pk, "song_id": song.pk}
        )
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
