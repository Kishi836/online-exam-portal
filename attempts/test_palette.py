"""FR-018 -- one question at a time with the four-state palette (Test Plan UT_043, UT_044, IT_021)."""
from django.test import TestCase
from django.urls import reverse

from portal.testkit import World
from repository.models import Answer

from .services import ANSWERED, MARKED, NOT_ANSWERED, NOT_VISITED, palette


class PaletteTests(TestCase):
    def setUp(self):
        self.world = World(n_questions=25)
        self.attempt = self.world.attempt()
        self.ids = [q.id for q in self.world.questions]
        self.client.force_login(self.world.stu_a)

    def open(self, n):
        return self.client.get(reverse("attempt-question", args=[self.attempt.pk, n]))

    def test_paper_url_redirects_to_question_1(self):
        response = self.client.get(reverse("attempt-paper", args=[self.attempt.pk]))
        self.assertRedirects(response, reverse("attempt-question", args=[self.attempt.pk, 1]))

    def test_UT_043_palette_moves_through_every_state(self):
        q5 = self.ids[4]
        self.assertEqual(palette(self.attempt, self.ids)[4], NOT_VISITED)
        # TODO(Kartik): open question 5 and assert NOT_ANSWERED; save option A for it with
        # services.save_answer and assert ANSWERED; set marked_for_review=True on its Answer row and
        # assert MARKED. Use q5 for the lookups.
        self.skipTest("TODO(Kartik): UT_043")

    def test_UT_044_exactly_one_stem_is_rendered(self):
        response = self.open(5)
        self.assertEqual(response.status_code, 200)
        # TODO(Kartik): assertContains "Question 5" exactly once (count=1 on the stem text), and for every
        # other question assertNotContains its stem. Careful: "Question 1" is a prefix of "Question 10".
        self.skipTest("TODO(Kartik): UT_044")

    def test_IT_021_states_survive_reload_because_they_come_from_the_server(self):
        # TODO(Kartik): produce all four states across ten questions (open some, answer some, mark one),
        # take palette(...), then use a brand-new Client logged in as STU_A (a "reloaded browser") to
        # open question 1 and assert response.context["cells"] gives the same states.
        self.skipTest("TODO(Kartik): IT_021")

    def test_question_out_of_range_is_404_and_other_students_attempt_is_404(self):
        self.assertEqual(self.open(26).status_code, 404)
        self.client.force_login(self.world.stu_b)
        self.assertEqual(self.open(1).status_code, 404)

    def test_revisiting_does_not_clear_a_saved_answer(self):
        # TODO(Kartik): save an answer to question 2, open question 2 again, assert the option is still saved.
        self.skipTest("TODO(Kartik): visit() must not overwrite")
