from carillon.models import Song
from django.views.generic import ListView


class SongView(ListView):
    model = Song
