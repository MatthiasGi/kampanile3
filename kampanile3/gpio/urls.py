from django.urls import include, path

from . import views

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
