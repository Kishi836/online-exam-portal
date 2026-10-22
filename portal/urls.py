from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

from identity.access import public
from identity.forms import EmailLoginForm

# /admin/ belongs to the Administrator role's pages (Test Plan), so Django's admin site moves aside.
urlpatterns = [
    path("django-admin/", admin.site.urls),
    path(
        "login/",
        public(auth_views.LoginView.as_view(authentication_form=EmailLoginForm)),
        name="login",
    ),
    path("logout/", public(auth_views.LogoutView.as_view()), name="logout"),
    path("", include("identity.urls")),
    path("", include("questionbank.urls")),
    path("", include("examsetup.urls")),
    path("", include("attempts.urls")),
]
