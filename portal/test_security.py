from django.test import Client, SimpleTestCase, override_settings
from django.urls import reverse


@override_settings(
    MIDDLEWARE=[
        "django.middleware.security.SecurityMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
        "identity.access.RoleMiddleware",
    ]
)
class CSRFProtectionTests(SimpleTestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=True)

    def test_login_post_without_csrf_token_is_rejected(self):
        response = self.client.post(
            reverse("login"),
            {"username": "test", "password": "invalid"},
        )
        self.assertEqual(response.status_code, 403)

    def test_logout_post_without_csrf_token_is_rejected(self):
        response = self.client.post(reverse("logout"))
        self.assertEqual(response.status_code, 403)
