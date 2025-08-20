from django.urls import include, path

from .views import carillon, song

app_name = "carillon"
urlpatterns = [
    path(
        "carillons/",
        include(
            (
                [
                    path("", carillon.CarillonListView.as_view(), name="list"),
                    path("add/", carillon.CarillonCreateView.as_view(), name="add"),
                    path(
                        "<int:pk>/",
                        carillon.CarillonDetailView.as_view(),
                        name="detail",
                    ),
                    path(
                        "<int:pk>/update/",
                        carillon.CarillonUpdateView.as_view(),
                        name="update",
                    ),
                    path(
                        "<int:pk>/delete/",
                        carillon.CarillonDeleteView.as_view(),
                        name="delete",
                    ),
                    path("<int:pk>/hit/", carillon.hit_note_view, name="hit_note"),
                    path("<int:pk>/stop/", carillon.stop_view, name="stop"),
                ],
                "carillons",
            )
        ),
    ),
    path(
        "songs/",
        include(
            (
                [
                    path("", song.SongView.as_view(), name="list"),
                    path(
                        "add/",
                        song.SongCreateView.as_view(),
                        name="add",
                    ),
                    path(
                        "<int:pk>/",
                        song.SongDetailView.as_view(),
                        name="detail",
                    ),
                    path(
                        "<int:pk>/update/",
                        song.SongUpdateView.as_view(),
                        name="update",
                    ),
                    path(
                        "<int:pk>/delete/",
                        song.SongDeleteView.as_view(),
                        name="delete",
                    ),
                    path("<int:pk>/play/", song.play_view, name="play"),
                ],
                "songs",
            )
        ),
    ),
]
