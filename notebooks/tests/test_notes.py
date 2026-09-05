from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from notebooks.models import Note, Notebook


class NoteLifecycleTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("maker", password="pw-maker-123")
        self.client.force_login(self.user)

    def test_new_note_seeds_content_from_type_template(self):
        notebook = Notebook.objects.create(
            owner=self.user, label="Class", notebook_type="class"
        )
        resp = self.client.post(
            reverse("note_create", kwargs={"pk": notebook.pk})
        )
        self.assertEqual(resp.status_code, 302)
        note = notebook.notes.get()
        self.assertIn("Key concepts:", note.content)
        self.assertEqual(note.position, 1)

    def test_blank_notebook_new_note_is_empty(self):
        notebook = Notebook.objects.create(
            owner=self.user, label="Scratch", notebook_type="blank"
        )
        self.client.post(reverse("note_create", kwargs={"pk": notebook.pk}))
        self.assertEqual(notebook.notes.get().content, "")

    def test_soft_delete_hides_note_but_keeps_row(self):
        notebook = Notebook.objects.create(owner=self.user, label="Book")
        note = Note.objects.create(notebook=notebook, title="Bye", position=1)

        resp = self.client.post(
            reverse(
                "note_delete",
                kwargs={"pk": notebook.pk, "note_pk": note.pk},
            )
        )
        self.assertEqual(resp.status_code, 302)

        self.assertFalse(Note.objects.filter(pk=note.pk).exists())
        self.assertTrue(Note.all_objects.filter(pk=note.pk).exists())
        Note.all_objects.get(pk=note.pk)  # still retrievable for trash later

        open_resp = self.client.get(
            reverse("notebook_open", kwargs={"pk": notebook.pk})
        )
        self.assertNotContains(open_resp, "Bye")

    def test_second_note_gets_next_position(self):
        notebook = Notebook.objects.create(owner=self.user, label="Ordered")
        self.client.post(reverse("note_create", kwargs={"pk": notebook.pk}))
        self.client.post(reverse("note_create", kwargs={"pk": notebook.pk}))
        positions = sorted(notebook.notes.values_list("position", flat=True))
        self.assertEqual(positions, [1, 2])


class SignupTests(TestCase):
    def test_signup_creates_user_and_lands_on_shelf(self):
        resp = self.client.post(
            reverse("signup"),
            data={
                "username": "newbie",
                "password1": "paper-nest-9182",
                "password2": "paper-nest-9182",
            },
        )
        self.assertRedirects(resp, reverse("shelf"))
        self.assertTrue(User.objects.filter(username="newbie").exists())


class LandingTests(TestCase):
    def test_anonymous_visitor_sees_welcome_with_links(self):
        resp = self.client.get(reverse("root"))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "accounts/landing.html")
        self.assertContains(resp, reverse("signup"))
        self.assertContains(resp, reverse("login"))

    def test_signed_in_visitor_is_sent_to_shelf(self):
        User.objects.create_user("already", password="pw-already-123")
        self.client.force_login(User.objects.get(username="already"))
        resp = self.client.get(reverse("root"))
        self.assertRedirects(resp, reverse("shelf"))
