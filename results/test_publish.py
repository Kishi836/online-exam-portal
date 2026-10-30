"""FR-025 / FR-026 -- results are withheld until Faculty publishes, and can be unpublished
(Test Plan UT_059, UT_060, UT_061, IT_032, IT_033)."""
from decimal import Decimal  # noqa: F401  (UT_061)

from django.test import TestCase
from django.urls import reverse

from portal.testkit import World

from .services import ResultsNotReady, set_results_published  # noqa: F401


class PublishTests(TestCase):
    def setUp(self):
        self.world = World(n_questions=25)
        self.attempt = self.world.submitted(right=16, wrong=0)  # 32 of 50, as in the Test Plan data
        self.world.close_window()

    def as_student(self, student=None):
        self.client.force_login(student or self.world.stu_a)

    def publish(self, value):
        self.client.force_login(self.world.fac_a)
        return self.client.post(reverse("results-publish", args=[self.world.exam.pk]), {"publish": value})

    def test_UT_059_unpublished_result_is_withheld(self):
        self.as_student()
        response = self.client.get(reverse("attempt-paper", args=[self.attempt.pk]))
        # TODO(Komal): assertContains "Results not yet published"; assertNotContains "32", "64" and "Pass".
        self.skipTest("TODO(Komal): UT_059")

    def test_UT_060_publishing_makes_the_result_visible(self):
        # TODO(Komal): self.publish("1"); then as STU_A the submitted page shows 32.00, 64.00 and Pass.
        self.skipTest("TODO(Komal): UT_060")

    def test_UT_061_unpublishing_withdraws_it_and_keeps_the_score(self):
        # TODO(Komal): publish, unpublish, then "Results not yet published" is back, and
        # attempt.refresh_from_db() still has score Decimal("32").
        self.skipTest("TODO(Komal): UT_061")

    def test_IT_032_unpublished_result_is_403_through_the_api(self):
        self.as_student()
        response = self.client.get(reverse("result-api", args=[self.attempt.pk]))
        self.assertEqual(response.status_code, 403)
        self.assertNotContains(response, "32", status_code=403)

    def test_IT_033_another_students_result_is_403(self):
        other = self.world.submitted(self.world.stu_b, right=5)
        set_results_published(self.world.exam, True)
        self.as_student()
        # TODO(Komal): GET result-api for `other` -> 403 and STU_B's score ("10.00") not in the body.
        # Then GET it for STU_A's own attempt -> 200 and response.json()["score"] == "32.00".
        self.skipTest("TODO(Komal): IT_033")

    def test_publishing_before_the_window_closes_is_refused(self):
        # TODO(Komal): make a fresh exam whose window_end is in the future (or None), and assert
        # set_results_published(exam, True) raises ResultsNotReady and results_published stays False.
        self.skipTest("TODO(Komal): FR-026 refuses early publication")

    def test_only_the_courses_faculty_can_publish(self):
        # TODO(Komal): a second Faculty not assigned to the course POSTs results-publish -> 403.
        self.skipTest("TODO(Komal): FR-003 on the publish endpoint")
