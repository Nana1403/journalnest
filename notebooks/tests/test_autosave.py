import json

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from notebooks.models import Note, Notebook


class AutosaveTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("writer", password="pw-writer-123")
        self.client.force_login(self.user)
        self.notebook = Notebook.objects.create(owner=self.user, label="Notes")
        self.note = Note.objects.create(
            notebook=self.notebook, title="Draft", content="", position=1
        )
        self.url = reverse(
            "note_autosave",
            kwargs={"pk": self.notebook.pk, "note_pk": self.note.pk},
        )

    def _post(self, payload):
        return self.client.post(
            self.url, data=json.dumps(payload), content_type="application/json"
        )

    def test_happy_path_bumps_revision(self):
        resp = self._post({"title": "Draft v2", "content": "hello", "revision": 1})
        self.assertEqual(resp.status_code, 200)
        body = resp.json()
        self.assertEqual(body["status"], "saved")
        self.assertEqual(body["revision"], 2)
        self.note.refresh_from_db()
        self.assertEqual(self.note.title, "Draft v2")
        self.assertEqual(self.note.content, "hello")
        self.assertEqual(self.note.revision, 2)

    def test_stale_revision_returns_conflict_and_keeps_server_copy(self):
        Note.objects.filter(pk=self.note.pk).update(
            revision=5, title="Server wins", content="server text"
        )
        resp = self._post({"title": "mine", "content": "my text", "revision": 1})
        self.assertEqual(resp.status_code, 409)
        body = resp.json()
        self.assertEqual(body["status"], "conflict")
        self.assertEqual(body["server"]["title"], "Server wins")
        self.assertEqual(body["server"]["content"], "server text")
        self.assertEqual(body["server"]["revision"], 5)
        self.note.refresh_from_db()
        self.assertEqual(self.note.title, "Server wins")

    def test_missing_title_is_rejected(self):
        resp = self._post({"content": "x", "revision": 1})
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.json()["status"], "invalid")

    def test_blank_title_is_rejected(self):
        resp = self._post({"title": "   ", "content": "x", "revision": 1})
        self.assertEqual(resp.status_code, 400)

    def test_extra_field_is_rejected(self):
        resp = self._post(
            {"title": "ok", "content": "x", "revision": 1, "surprise": True}
        )
        self.assertEqual(resp.status_code, 400)

    def test_oversized_content_is_rejected(self):
        resp = self._post(
            {"title": "ok", "content": "a" * 100_001, "revision": 1}
        )
        self.assertEqual(resp.status_code, 400)

    def test_get_not_allowed(self):
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 405)
