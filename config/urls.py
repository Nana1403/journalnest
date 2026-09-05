from django.contrib import admin
from django.urls import include, path

from accounts.views import landing

urlpatterns = [
    path("", landing, name="root"),
    path("admin/", admin.site.urls),
    path("", include("accounts.urls")),
    path("", include("notebooks.urls")),
]
