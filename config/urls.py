from django.contrib import admin
from django.shortcuts import redirect
from django.urls import include, path


def root(request):
    """Send visitors to their shelf, or to the login page if signed out."""
    if request.user.is_authenticated:
        return redirect("shelf")
    return redirect("login")


urlpatterns = [
    path("", root, name="root"),
    path("admin/", admin.site.urls),
    path("", include("accounts.urls")),
    path("", include("notebooks.urls")),
]
