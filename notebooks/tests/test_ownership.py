import json

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from notebooks.models import Note, Notebook


class OwnershipTests(TestCase):
    def setUp(self):
        self.alice = User.objects.create_user("alice", password="pw-alice-123")
        self.bob = User.objects.create_user("bob", password="pw-bob-12345")
        self.notebook = Notebook.objects.create(owner=self.alice, label="Alice's book")
        self.note = Note.objects.create(
            notebook=self.notebook, title="Secret", content="hush", position=1
        )

    def test_bob_cannot_open_alices_notebook(self):
        self.client.force_login(self.bob)
        resp = self.client.get(
            reverse("notebook_open", kwargs={"pk": self.notebook.pk})
        )
        self.assertEqual(resp.status_code, 404)

    def test_bob_cannot_autosave_alices_note(self):
        self.client.force_login(self.bob)
        resp = self.client.post(
            reverse(
                "note_autosave",
                kwargs={"pk": self.notebook.pk, "note_pk": self.note.pk},
            ),
            data=json.dumps({"title": "hacked", "content": "x", "revision": 1}),
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, 404)
        self.note.refresh_from_db()
        self.assertEqual(self.note.title, "Secret")

    def test_bob_cannot_customize_alices_notebook(self):
        self.client.force_login(self.bob)
        resp = self.client.post(
            reverse("notebook_customize", kwargs={"pk": self.notebook.pk}),
            data=json.dumps(
                {
                    "label": "mine now",
                    "label_font": "caveat",
                    "cover_color": "sage",
                    "cover_pattern": "dots",
                    "notebook_type": "blank",
                    "sticker_layout": [],
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, 404)

    def test_bob_cannot_delete_alices_note(self):
        self.client.force_login(self.bob)
        resp = self.client.post(
            reverse(
                "note_delete",
                kwargs={"pk": self.notebook.pk, "note_pk": self.note.pk},
            )
        )
        self.assertEqual(resp.status_code, 404)
        self.note.refresh_from_db()
        self.assertIsNone(self.note.deleted_at)

    def test_anonymous_shelf_redirects_to_login(self):
        resp = self.client.get(reverse("shelf"))
        self.assertEqual(resp.status_code, 302)
        self.assertIn(reverse("login"), resp["Location"])
