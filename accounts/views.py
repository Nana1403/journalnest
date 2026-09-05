from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import SignUpForm


def landing(request):
    """Friendly welcome page for signed-out visitors."""
    if request.user.is_authenticated:
        return redirect("shelf")
    return render(request, "accounts/landing.html")


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = "accounts/signup.html"
    success_url = reverse_lazy("shelf")

    def form_valid(self, form):
        response = super().form_valid(form)
        # Log the new account in immediately so they land on their shelf.
        login(self.request, self.object)
        return response
