from django.contrib.auth.decorators import login_required
from django.db.models import Max
from django.http import HttpResponseNotAllowed, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_POST

from .constants import PAGE_TEMPLATES
from .forms import NotebookForm
from .models import Note, Notebook
from .schemas import AutosavePayload, NotebookCustomization, SchemaError, parse_body


def _get_notebook(request, pk) -> Notebook:
    """Fetch a notebook the current user owns, or 404."""
    return get_object_or_404(Notebook, pk=pk, owner=request.user)


def _get_note(request, notebook_pk, note_pk) -> Note:
    """Fetch a live note inside a notebook the current user owns, or 404."""
    return get_object_or_404(
        Note, pk=note_pk, notebook__pk=notebook_pk, notebook__owner=request.user
    )


@login_required
def shelf(request):
    notebooks = request.user.notebooks.all()
    return render(request, "notebooks/shelf.html", {"notebooks": notebooks})


@login_required
def notebook_create(request):
    if request.method == "POST":
        form = NotebookForm(request.POST)
        if form.is_valid():
            notebook = form.save(commit=False)
            notebook.owner = request.user
            notebook.save()
            return redirect("notebook_open", pk=notebook.pk)
    else:
        form = NotebookForm()
    return render(request, "notebooks/notebook_form.html", {"form": form})


@login_required
def notebook_open(request, pk):
    notebook = _get_notebook(request, pk)
    notes = list(notebook.notes.all())

    selected = None
    requested = request.GET.get("note")
    if requested:
        selected = next((n for n in notes if str(n.pk) == requested), None)
    if selected is None and notes:
        selected = notes[0]

    prev_note = next_note = None
    if selected is not None:
        index = notes.index(selected)
        if index > 0:
            prev_note = notes[index - 1]
        if index < len(notes) - 1:
            next_note = notes[index + 1]

    return render(
        request,
        "notebooks/notebook.html",
        {
            "notebook": notebook,
            "notes": notes,
            "note": selected,
            "prev_note": prev_note,
            "next_note": next_note,
        },
    )


@login_required
@require_POST
def note_create(request, pk):
    notebook = _get_notebook(request, pk)
    next_position = (
        notebook.notes.aggregate(m=Max("position"))["m"] or 0
    ) + 1
    note = Note.objects.create(
        notebook=notebook,
        title="Untitled note",
        content=PAGE_TEMPLATES.get(notebook.notebook_type, ""),
        position=next_position,
    )
    open_url = reverse("notebook_open", kwargs={"pk": notebook.pk})
    return redirect(f"{open_url}?note={note.pk}")


@login_required
@require_POST
def note_delete(request, pk, note_pk):
    note = _get_note(request, pk, note_pk)
    note.deleted_at = timezone.now()
    note.save(update_fields=["deleted_at", "updated_at"])
    return redirect("notebook_open", pk=pk)


@login_required
def note_autosave(request, pk, note_pk):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    note = _get_note(request, pk, note_pk)

    try:
        payload = parse_body(request, AutosavePayload)
    except SchemaError as exc:
        return JsonResponse({"status": "invalid", "errors": exc.errors}, status=400)

    if payload.revision != note.revision:
        # Another tab saved first. Never overwrite it silently.
        return JsonResponse(
            {
                "status": "conflict",
                "server": {
                    "title": note.title,
                    "content": note.content,
                    "revision": note.revision,
                    "updated_at": note.updated_at.isoformat(),
                },
            },
            status=409,
        )

    note.title = payload.title
    note.content = payload.content
    note.revision += 1
    note.save(update_fields=["title", "content", "revision", "updated_at"])

    return JsonResponse(
        {
            "status": "saved",
            "revision": note.revision,
            "saved_at": note.updated_at.isoformat(),
        }
    )


@login_required
@require_POST
def notebook_customize(request, pk):
    notebook = _get_notebook(request, pk)

    try:
        payload = parse_body(request, NotebookCustomization)
    except SchemaError as exc:
        return JsonResponse({"status": "invalid", "errors": exc.errors}, status=400)

    notebook.label = payload.label
    notebook.label_font = payload.label_font
    notebook.cover_color = payload.cover_color
    notebook.cover_pattern = payload.cover_pattern
    notebook.notebook_type = payload.notebook_type
    notebook.sticker_layout = [s.model_dump() for s in payload.sticker_layout]
    notebook.save()

    cover_html = render_to_string(
        "notebooks/_cover.html", {"notebook": notebook}, request=request
    )
    return JsonResponse({"status": "saved", "cover_html": cover_html})
