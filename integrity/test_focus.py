"""FR-028 -- focus-loss events with a server timestamp (Test Plan UT_064, UT_065, UT_066, UT_067).

The browser half (focus.js firing once per switch) is checked by hand in Chrome / Edge / Firefox;
these tests cover the server half: one POST is one event, the time is the server's, nothing else is trusted.
"""
from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from portal.testkit import World
from repository.models import FocusEvent


class FocusTests(TestCase):
    def setUp(self):
        self.world = World()
        self.attempt = self.world.attempt()
        self.client.force_login(self.world.stu_a)
        self.url = reverse("attempt-focus-lost", args=[self.attempt.pk])

    def test_UT_064_one_focus_loss_is_one_event_with_a_server_time(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 204)
        # TODO(Kartik): exactly one FocusEvent for self.attempt, occurred_at within a few seconds of timezone.now().
        self.skipTest("TODO(Kartik): UT_064")

    def test_UT_065_three_losses_are_three_events(self):
        # TODO(Kartik): POST three times; three events, each with its own occurred_at (non-decreasing).
        self.skipTest("TODO(Kartik): UT_065")

    def test_UT_066_no_loss_means_no_event(self):
        # TODO(Kartik): open the attempt page and save an answer (attempt-answer), never POST focus-lost;
        # the event log for the attempt is empty.
        self.skipTest("TODO(Kartik): UT_066")

    def test_UT_067_client_supplied_time_is_ignored(self):
        fake = (timezone.now() + timedelta(hours=1)).isoformat()
        # TODO(Kartik): POST with data {"occurred_at": fake, "at": fake} and HTTP_DATE=fake;
        # the stored time is still within seconds of the real server now, not an hour ahead.
        self.skipTest("TODO(Kartik): UT_067")

    def test_submitted_attempt_refuses_new_events(self):
        # TODO(Kartik): submit the attempt (attempts.services.submit), POST -> 409, no event stored.
        self.skipTest("TODO(Kartik): closed attempt")

    def test_another_students_attempt_is_404(self):
        self.client.force_login(self.world.stu_b)
        self.assertEqual(self.client.post(self.url).status_code, 404)
        self.assertFalse(FocusEvent.objects.exists())

    def test_faculty_integrity_page_lists_each_attempts_events(self):
        # TODO(Kartik): two events on STU_A's attempt; as FAC_A GET exam-integrity -> 200, shows STU_A
        # with "2". A Faculty not on the course -> 403. A Student -> 403.
        self.skipTest("TODO(Kartik): Faculty integrity page")
