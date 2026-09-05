from django.urls import path

from . import views

urlpatterns = [
    path("shelf/", views.shelf, name="shelf"),
    path("notebooks/new/", views.notebook_create, name="notebook_create"),
    path("notebooks/<uuid:pk>/", views.notebook_open, name="notebook_open"),
    path(
        "notebooks/<uuid:pk>/customize/",
        views.notebook_customize,
        name="notebook_customize",
    ),
    path(
        "notebooks/<uuid:pk>/notes/new/",
        views.note_create,
        name="note_create",
    ),
    path(
        "notebooks/<uuid:pk>/notes/<uuid:note_pk>/autosave/",
        views.note_autosave,
        name="note_autosave",
    ),
    path(
        "notebooks/<uuid:pk>/notes/<uuid:note_pk>/delete/",
        views.note_delete,
        name="note_delete",
    ),
]
