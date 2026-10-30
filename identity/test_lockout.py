"""NFR-012 -- lock an account for 15 minutes after 5 failed sign-ins within 15 minutes.

SRS pass condition: the 6th sign-in attempt after 5 failures is refused even with the right password,
and succeeds after 15 minutes.
"""
from datetime import timedelta  # noqa: F401  (for the TODO tests)

from django.test import TestCase
from django.urls import reverse

from portal.testkit import PASSWORD, World
from repository.models import SignInFailure  # noqa: F401

LOCKED = "Too many failed sign-ins"


class LockoutTests(TestCase):
    def setUp(self):
        self.world = World(n_questions=1)
        self.email = self.world.stu_a.email

    def sign_in(self, password, email=None):
        return self.client.post(reverse("login"), {"email": email or self.email, "password": password})

    def fail(self, times, email=None):
        for _ in range(times):
            self.sign_in("wrong-password", email)

    def test_four_failures_then_right_password_signs_in(self):
        self.fail(4)
        # TODO(Komal): sign_in(PASSWORD) redirects (302) and the user is authenticated ("_auth_user_id" in session).
        self.skipTest("TODO(Komal): below the threshold")

    def test_sixth_attempt_with_right_password_is_refused(self):
        self.fail(5)
        response = self.sign_in(PASSWORD)
        self.assertContains(response, LOCKED)
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_lock_lifts_after_15_minutes(self):
        self.fail(5)
        # TODO(Komal): age every SignInFailure row by 16 minutes
        # (SignInFailure.objects.update(at=F("at") - timedelta(minutes=16)) -- at is auto_now_add, so update() it),
        # then sign_in(PASSWORD) succeeds.
        self.skipTest("TODO(Komal): unlock after 15 minutes")

    def test_failures_older_than_15_minutes_do_not_count(self):
        # TODO(Komal): 3 failures aged 20 minutes + 2 fresh ones -> not locked.
        self.skipTest("TODO(Komal): sliding window")

    def test_unknown_email_is_counted_and_gives_the_same_message(self):
        self.fail(5, email="nobody@pesu.pes.edu")
        # TODO(Komal): 5 rows for that email; a 6th try shows the same LOCKED text a real account would.
        self.skipTest("TODO(Komal): no account enumeration")

    def test_success_clears_the_count(self):
        # TODO(Komal): 4 failures, a success, sign out, 4 more failures -> still not locked.
        self.skipTest("TODO(Komal): clear on success")

    def test_email_case_does_not_dodge_the_lock(self):
        # TODO(Komal): 5 failures as STU.A@PESU.PES.EDU lock stu.a@pesu.pes.edu too.
        self.skipTest("TODO(Komal): case-insensitive")
