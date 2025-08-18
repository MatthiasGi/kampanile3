from django.urls import include, path
from django.views.generic import TemplateView

from . import views

app_name = "frontend"
urlpatterns = [
    path("", TemplateView.as_view(template_name="frontend/index.html"), name="index"),
    path(
        "songs/",
        include(
            (
                [
                    path("", views.SongView.as_view(), name="list"),
                ],
                "songs",
            )
        ),
    ),
]
