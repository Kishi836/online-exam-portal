"""The Test Plan's standard data (STU_A, STU_B, FAC_A, ADM_A, CRS_X, EXM_1) for the Sprint 2 tests to share."""
from datetime import timedelta
from decimal import Decimal

from django.utils import timezone

from repository.models import Attempt, Course, Exam, ExamQuestion, Option, Question, Role, User

PASSWORD = "Passw0rd!A"


def make_user(role, email, **extra):
    extra.setdefault("full_name", email.split("@")[0])
    return User.objects.create_user(email, PASSWORD, role=role, **extra)


class World:
    """One course, one Faculty, two enrolled Students and a published EXM_1 whose window is open now.

    EXM_1 has `n_questions` questions of +2 / -0.5, each with option A (correct) and option B (wrong).
    """

    def __init__(self, n_questions=5, opens_in=timedelta(hours=-1), closes_in=timedelta(hours=1)):
        self.stu_a = make_user(Role.STUDENT, "stu.a@pesu.pes.edu", roll_number="PES1UG24CS001")
        self.stu_b = make_user(Role.STUDENT, "stu.b@pesu.pes.edu", roll_number="PES1UG24CS002")
        self.fac_a = make_user(Role.FACULTY, "fac.a@pes.edu")
        self.adm_a = make_user(Role.ADMIN, "adm.a@pes.edu")
        self.course = Course.objects.create(code="UE24CS341A", title="Software Engineering", semester=5)
        self.course.faculty.add(self.fac_a)
        self.course.students.add(self.stu_a, self.stu_b)
        now = timezone.now()
        self.exam = Exam.objects.create(
            course=self.course, title="EXM_1", duration_minutes=60, total_marks=Decimal(2 * n_questions),
            pass_mark_percent=Decimal("40"), status=Exam.Status.PUBLISHED, published_at=now,
            window_start=now + opens_in, window_end=now + closes_in,
        )
        self.questions, self.right, self.wrong = [], [], []
        for i in range(n_questions):
            q = Question.objects.create(
                course=self.course, stem=f"Question {i + 1}", topic="t", difficulty=Question.Difficulty.EASY,
                positive_marks=Decimal("2"), negative_marks=Decimal("0.5"), created_by=self.fac_a,
            )
            ExamQuestion.objects.create(exam=self.exam, question=q, order=i)
            self.questions.append(q)
            self.right.append(Option.objects.create(question=q, text="A", is_correct=True))
            self.wrong.append(Option.objects.create(question=q, text="B"))

    def attempt(self, student=None):
        """An in-progress attempt, started now."""
        return Attempt.objects.create(exam=self.exam, student=student or self.stu_a)

    def submitted(self, student=None, right=0, wrong=0):
        """A submitted, evaluated attempt with `right` correct and `wrong` incorrect answers, in question order."""
        from attempts.services import save_answer, submit

        attempt = self.attempt(student)
        for option in self.right[:right] + self.wrong[right:right + wrong]:
            save_answer(attempt, option.question_id, option.pk)
        submit(attempt)
        return attempt

    def close_window(self):
        """Move EXM_1's window into the past, as if the examination has ended."""
        now = timezone.now()
        Exam.objects.filter(pk=self.exam.pk).update(window_start=now - timedelta(hours=3), window_end=now - timedelta(hours=1))
        self.exam.refresh_from_db()
