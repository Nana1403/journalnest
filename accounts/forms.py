from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    """Username + password sign-up, with an optional email address."""

    email = forms.EmailField(required=False)

    class Meta:
        model = User
        fields = ("username", "email")
