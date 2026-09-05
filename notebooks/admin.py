from django.contrib import admin

from .models import Note, Notebook


@admin.register(Notebook)
class NotebookAdmin(admin.ModelAdmin):
    list_display = ("label", "owner", "notebook_type", "is_favorite", "updated_at")
    list_filter = ("notebook_type", "is_favorite")
    search_fields = ("label", "owner__username")


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ("title", "notebook", "position", "revision", "deleted_at", "updated_at")
    list_filter = ("notebook",)
    search_fields = ("title", "content")

    def get_queryset(self, request):
        # Show soft-deleted notes in the admin too.
        return Note.all_objects.all()
