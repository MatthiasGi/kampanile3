from django.contrib import admin

from .models import Rule, Song

admin.site.register(Song)
admin.site.register(Rule)
