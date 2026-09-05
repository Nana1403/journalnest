import uuid

from django.conf import settings
from django.db import models

from .constants import (
    COLOR_CHOICES,
    FONT_CHOICES,
    PATTERN_CHOICES,
    TYPE_CHOICES,
)


class TimeStamped(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Notebook(TimeStamped):
    """A closed notebook on the shelf: a customizable cover plus its notes."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notebooks",
    )
    # The front label is the notebook's name; renaming it updates the cover
    # and any search results consistently.
    label = models.CharField(max_length=120)
    label_font = models.CharField(
        max_length=32, choices=FONT_CHOICES, default="caveat"
    )
    cover_color = models.CharField(
        max_length=16, choices=COLOR_CHOICES, default="cream"
    )
    cover_pattern = models.CharField(
        max_length=16, choices=PATTERN_CHOICES, default="plain"
    )
    # List of {"sticker": str, "x": float, "y": float, "rotation": float}.
    sticker_layout = models.JSONField(default=list, blank=True)
    notebook_type = models.CharField(
        max_length=16, choices=TYPE_CHOICES, default="blank"
    )
    is_favorite = models.BooleanField(default=False)

    class Meta:
        ordering = ["-is_favorite", "-updated_at"]

    def __str__(self):
        return self.label


class NoteManager(models.Manager):
    """Default manager that hides soft-deleted notes."""

    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)


class Note(TimeStamped):
    """A named entry inside a notebook, written on a paper-style page."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    notebook = models.ForeignKey(
        Notebook, on_delete=models.CASCADE, related_name="notes"
    )
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    position = models.PositiveIntegerField(default=0)
    # Bumped on every confirmed save; used to detect a competing edit from
    # another tab before overwriting it.
    revision = models.PositiveIntegerField(default=1)
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = NoteManager()
    all_objects = models.Manager()

    class Meta:
        ordering = ["position", "created_at"]

    def __str__(self):
        return self.title
