"""FR-003 -- one role per account, enforced on every screen and endpoint (Test Plan UC-02)."""
from django.db import IntegrityError, transaction
from django.http import HttpResponse
from django.test import TestCase, override_settings
from django.urls import include, path

from repository.models import Role, User

from .access import roles


@roles(Role.FACULTY)
def faculty_api(request):
    return HttpResponse("ok")


def undeclared_view(request):
    return HttpResponse("should never be reached")


urlpatterns = [
    path("", include("portal.urls")),
    path("api/questions", faculty_api),
    path("undeclared/", undeclared_view),
]


def make_user(role, email):
    return User.objects.create_user(email, "Passw0rd!A", full_name=email, role=role)


@override_settings(ROOT_URLCONF="identity.tests")
class RoleAccessTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.student = make_user(Role.STUDENT, "stu.a@pesu.pes.edu")
        cls.faculty = make_user(Role.FACULTY, "fac.a@pes.edu")
        cls.admin = make_user(Role.ADMIN, "admin@pes.edu")

    def test_account_without_a_valid_role_is_rejected_by_the_database(self):
        for bad_role in ("", "ROOT"):
            with self.subTest(role=bad_role), self.assertRaises(IntegrityError), transaction.atomic():
                make_user(bad_role, f"x{bad_role}@pes.edu")

    def test_IT_004_student_is_refused_faculty_screens_and_endpoints(self):
        self.client.force_login(self.student)
        self.assertEqual(self.client.get("/faculty/").status_code, 403)
        self.assertEqual(self.client.post("/api/questions").status_code, 403)

    def test_IT_005_faculty_is_refused_administrator_screens(self):
        self.client.force_login(self.faculty)
        self.assertEqual(self.client.get("/admin/").status_code, 403)

    def test_IT_006_unauthenticated_client_is_refused(self):
        response = self.client.get("/faculty/")
        self.assertRedirects(response, "/login/?next=/faculty/", fetch_redirect_response=False)
        self.assertEqual(self.client.post("/api/questions").status_code, 401)

    def test_view_that_declares_no_roles_is_refused_to_everyone(self):
        for user in (self.student, self.faculty, self.admin):
            self.client.force_login(user)
            self.assertEqual(self.client.get("/undeclared/").status_code, 403)

    def test_ST_002_each_role_lands_on_its_own_dashboard(self):
        for user, dashboard in (
            (self.student, "/student/"),
            (self.faculty, "/faculty/"),
            (self.admin, "/admin/"),
        ):
            self.client.force_login(user)
            self.assertRedirects(self.client.get("/"), dashboard)

    def test_sign_in_page_is_public(self):
        self.assertEqual(self.client.get("/login/").status_code, 200)
