from django.contrib import admin

from .models import Carillon, Rule, Song, Striker

admin.site.register(Carillon)
admin.site.register(Rule)
admin.site.register(Song)
admin.site.register(Striker)
