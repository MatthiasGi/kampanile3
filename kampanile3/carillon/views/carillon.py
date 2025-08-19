import json

from carillon.models import Carillon
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from ..forms import CarillonForm


class CarillonListView(ListView):
    model = Carillon


class CarillonDetailView(DetailView):
    model = Carillon


class CarillonCreateView(CreateView):
    model = Carillon
    form_class = CarillonForm


class CarillonUpdateView(UpdateView):
    model = Carillon
    form_class = CarillonForm


class CarillonDeleteView(DeleteView):
    model = Carillon


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
        print(str(e))
        return JsonResponse({"error": str(e)}, status=500)
