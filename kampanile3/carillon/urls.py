from django.urls import include, path

from .views import carillon, song, striker

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
                    path(
                        "<int:pk>/set-volume/",
                        carillon.set_volume_view,
                        name="set_volume",
                    ),
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
                    path("", song.SongListView.as_view(), name="list"),
                    path("add/", song.SongCreateView.as_view(), name="add"),
                    path("<int:pk>/", song.SongDetailView.as_view(), name="detail"),
                    path(
                        "<int:pk>/update/", song.SongUpdateView.as_view(), name="update"
                    ),
                    path(
                        "<int:pk>/delete/", song.SongDeleteView.as_view(), name="delete"
                    ),
                    path("<int:pk>/play/", song.play_view, name="play"),
                ],
                "songs",
            )
        ),
    ),
    path(
        "strikers/",
        include(
            (
                [
                    path("", striker.StrikerListView.as_view(), name="list"),
                    path("add/", striker.StrikerCreateView.as_view(), name="add"),
                    path(
                        "<int:pk>/", striker.StrikerDetailView.as_view(), name="detail"
                    ),
                    path(
                        "<int:pk>/update/",
                        striker.StrikerUpdateView.as_view(),
                        name="update",
                    ),
                    path(
                        "<int:pk>/delete/",
                        striker.StrikerDeleteView.as_view(),
                        name="delete",
                    ),
                    path(
                        "<int:pk>/add-rule/",
                        striker.StrikerRuleCreateView.as_view(),
                        name="add_rule",
                    ),
                ],
                "strikers",
            ),
        ),
    ),
    path(
        "strikers/rules/",
        include(
            (
                [
                    path(
                        "<int:pk>/",
                        striker.StrikerRuleDetailView.as_view(),
                        name="detail",
                    ),
                    path(
                        "<int:pk>/update/",
                        striker.StrikerRuleUpdateView.as_view(),
                        name="update",
                    ),
                    path(
                        "<int:pk>/delete/",
                        striker.StrikerRuleDeleteView.as_view(),
                        name="delete",
                    ),
                ],
                "rules",
            )
        ),
    ),
]
