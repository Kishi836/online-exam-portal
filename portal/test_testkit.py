"""The shared test data builds what the Test Plan describes."""
from decimal import Decimal

from django.test import TestCase

from .testkit import World


class WorldTests(TestCase):
    def test_submitted_attempt_is_evaluated_with_per_question_marks(self):
        world = World(n_questions=5)
        attempt = world.submitted(right=3, wrong=1)
        self.assertEqual(attempt.score, Decimal("5.5"))  # 3 x 2 - 1 x 0.5
        self.assertEqual(sorted(attempt.answers.values_list("marks", flat=True)), [Decimal("-0.5"), 2, 2, 2])
