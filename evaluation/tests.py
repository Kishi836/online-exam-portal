"""FR-022, FR-023 -- automatic evaluation and the marking rule (Test Plan UC-11)."""
from decimal import Decimal

from django.test import SimpleTestCase, TestCase

from attempts.services import submit
from repository.models import Answer, Attempt, Course, Exam, ExamQuestion, Option, Question, Role, User

from .engine import evaluate, marks_for


class MarkingRuleTests(SimpleTestCase):
    """UT_053 -- UT_056: Q_SC1 = +2 / -0.5, correct option B. No database needed."""

    def setUp(self):
        self.question = Question(positive_marks=Decimal("2"), negative_marks=Decimal("0.5"))
        self.a = Option(question=self.question, is_correct=False)
        self.b = Option(question=self.question, is_correct=True)

    def test_UT_053_correct_response_earns_full_positive_marks(self):
        self.assertEqual(marks_for(self.question, self.b, negative_marking=True), Decimal("2"))

    def test_UT_054_incorrect_response_loses_the_configured_negative_marks(self):
        self.assertEqual(marks_for(self.question, self.a, negative_marking=True), Decimal("-0.5"))

    def test_UT_055_unanswered_question_earns_zero_with_no_deduction(self):
        self.assertEqual(marks_for(self.question, None, negative_marking=True), Decimal("0"))

    def test_UT_056_no_deduction_when_negative_marking_is_disabled(self):
        self.assertEqual(marks_for(self.question, self.a, negative_marking=False), Decimal("0"))


class EvaluationTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.faculty = User.objects.create_user("fac.a@pes.edu", "Passw0rd!A", full_name="Fac A", role=Role.FACULTY)
        cls.course = Course.objects.create(code="UE24CS341A", title="Software Engineering", semester=5)

    def make_exam(self, n_questions):
        """An exam of n questions at +2 / -0.5; returns the exam and each question's (wrong, right) options."""
        exam = Exam.objects.create(
            course=self.course, title="EXM_1", duration_minutes=60,
            total_marks=2 * n_questions, pass_mark_percent=40,
        )
        options = []
        for i in range(n_questions):
            q = Question.objects.create(
                course=self.course, stem=f"Q{i}", topic="t", difficulty=Question.Difficulty.EASY,
                positive_marks=2, negative_marks=Decimal("0.5"), created_by=self.faculty,
            )
            ExamQuestion.objects.create(exam=exam, question=q, order=i)
            options.append((Option.objects.create(question=q, text="A"), Option.objects.create(question=q, text="B", is_correct=True)))
        return exam, options

    def sit(self, exam, options, n_correct, n_wrong, email="stu.a@pesu.pes.edu"):
        """A Student answers the first n_correct right, the next n_wrong wrong, and skips the rest."""
        student = User.objects.create_user(email, "Passw0rd!A", full_name=email, role=Role.STUDENT)
        attempt = Attempt.objects.create(exam=exam, student=student)
        for i, (wrong, right) in enumerate(options):
            chosen = right if i < n_correct else wrong if i < n_correct + n_wrong else None
            Answer.objects.create(attempt=attempt, question=right.question, option=chosen)
        return attempt

    def test_FR_023_srs_example_10_correct_4_wrong_6_unanswered_scores_18(self):
        exam, options = self.make_exam(20)
        self.assertEqual(evaluate(self.sit(exam, options, 10, 4)), Decimal("18"))

    def test_IT_031_mixed_attempt_is_scored_end_to_end(self):
        exam, options = self.make_exam(10)
        attempt = self.sit(exam, options, 6, 3)
        submit(attempt)
        attempt.refresh_from_db()
        self.assertEqual(attempt.score, Decimal("10.5"))

    def test_question_with_no_answer_row_counts_as_unanswered(self):
        exam, options = self.make_exam(3)
        attempt = self.sit(exam, options, 1, 1)
        attempt.answers.filter(option__isnull=True).delete()
        self.assertEqual(evaluate(attempt), Decimal("1.5"))

    def test_IT_029_every_submitted_attempt_is_evaluated_without_faculty_action(self):
        exam, options = self.make_exam(5)
        attempts = [self.sit(exam, options, c, 1, email=f"stu{c}@pesu.pes.edu") for c in (0, 2, 4)]
        for attempt in attempts:
            submit(attempt)
        scores = list(Attempt.objects.filter(exam=exam).order_by("student__email").values_list("submitted_at", "score"))
        self.assertTrue(all(submitted and score is not None for submitted, score in scores))
        self.assertEqual([s for _, s in scores], [Decimal("-0.5"), Decimal("3.5"), Decimal("7.5")])

    def test_submitting_twice_keeps_the_first_submission(self):
        exam, options = self.make_exam(2)
        attempt = self.sit(exam, options, 2, 0)
        submit(attempt)
        first = Attempt.objects.get(pk=attempt.pk).submitted_at
        attempt.answers.update(option=None)
        submit(attempt)
        attempt.refresh_from_db()
        self.assertEqual((attempt.submitted_at, attempt.score), (first, Decimal("4")))
