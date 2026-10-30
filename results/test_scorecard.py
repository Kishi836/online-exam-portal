"""FR-027 -- the Student scorecard with per-question marks (Test Plan UT_062, UT_063, ST_012)."""
from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from portal.testkit import World
from repository.models import Exam

from .services import scorecard


class ScorecardTests(TestCase):
    def setUp(self):
        self.world = World(n_questions=25)
        # 17 right, 4 wrong, 4 unanswered: 34 - 2 = 32 of 50 -> 64%, Pass at 40% (the Test Plan's figures).
        self.attempt = self.world.submitted(right=17, wrong=4)
        Exam.objects.filter(pk=self.world.exam.pk).update(results_published=True)
        self.attempt.refresh_from_db()
        self.client.force_login(self.world.stu_a)

    def test_figures_match_the_test_plan(self):
        self.assertEqual((self.attempt.score, self.attempt.percentage, self.attempt.passed), (Decimal("32"), Decimal("64"), True))

    def test_UT_062_scorecard_shows_total_percentage_outcome_and_every_question(self):
        response = self.client.get(reverse("scorecard", args=[self.attempt.pk]))
        self.assertEqual(response.status_code, 200)
        # TODO(Kartik): assertContains "32.00", "64.00" and "Pass"; exactly 25 rows in card["rows"];
        # the negatives show as -0.50 and unanswered ones as 0 / "Not answered".
        self.skipTest("TODO(Kartik): UT_062")

    def test_UT_063_per_question_marks_sum_to_the_total(self):
        card = scorecard(self.attempt)
        # TODO(Kartik): assertEqual(sum(row["marks"] for row in card["rows"]), card["score"])
        self.skipTest("TODO(Kartik): UT_063")

    def test_ST_012_every_scorecard_matches_the_stored_evaluation(self):
        # TODO(Kartik): five Students (make three more with portal.testkit.make_user + enroll them),
        # each with a different right/wrong mix; for each, the scorecard page shows exactly the stored
        # score, percentage and outcome of their own Attempt row.
        self.skipTest("TODO(Kartik): ST_012")

    def test_unpublished_scorecard_is_403(self):
        Exam.objects.filter(pk=self.world.exam.pk).update(results_published=False)
        self.assertEqual(self.client.get(reverse("scorecard", args=[self.attempt.pk])).status_code, 403)

    def test_another_students_scorecard_is_403(self):
        self.client.force_login(self.world.stu_b)
        self.assertEqual(self.client.get(reverse("scorecard", args=[self.attempt.pk])).status_code, 403)

    def test_scorecard_never_reveals_the_correct_option(self):
        # TODO(Kartik): for an answered-wrong question, the page must not say which option was correct
        # (the text "A" appears only where the Student chose A).
        self.skipTest("TODO(Kartik): no answer key on the scorecard")
