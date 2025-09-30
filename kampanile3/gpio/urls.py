from django.conf import settings
from django.urls import include, path

from . import lib, views

app_name = "gpio"
urlpatterns = [
    path(
        "inputs/",
        include(
            (
                [
                    path("", views.InputListView.as_view(), name="list"),
                    path("add/", views.InputCreateView.as_view(), name="add"),
                    path("<int:pk>/", views.InputDetailView.as_view(), name="detail"),
                    path(
                        "<int:pk>/update/",
                        views.InputUpdateView.as_view(),
                        name="update",
                    ),
                    path(
                        "<int:pk>/delete/",
                        views.InputDeleteView.as_view(),
                        name="delete",
                    ),
                ],
                "inputs",
            )
        ),
    )
]


if settings.RUNNING_SERVER and settings.GPIO:
    lib.init_thread()
