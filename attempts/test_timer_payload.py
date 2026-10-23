from datetime import timedelta
from decimal import Decimal

from django.test import TestCase
from django.utils import timezone

from repository.models import Attempt, Course, Exam, Option, Question, Role, User

from .payload import question_for_student
from .timer import remaining_seconds


def make_user(role, email, password="Passw0rd!A", **extra):
    return User.objects.create_user(email, password, full_name=email, role=role, **extra)


class TimerAndPayloadTests(TestCase):
    def setUp(self):
        self.student = make_user(Role.STUDENT, "stu.a@pesu.pes.edu", roll_number="PES1UG24CS001")
        self.other_student = make_user(Role.STUDENT, "stu.b@pesu.pes.edu", roll_number="PES1UG24CS002")
        self.faculty = make_user(Role.FACULTY, "fac.a@pes.edu")
        self.course = Course.objects.create(code="UE24CS351A", title="Database Management Systems", semester=5)
        self.course.faculty.add(self.faculty)
        self.question = Question.objects.create(
            course=self.course,
            stem="Which normal form removes transitive dependency?",
            topic="Normalization",
            difficulty=Question.Difficulty.MEDIUM,
            positive_marks=Decimal("2"),
            negative_marks=Decimal("0.5"),
            created_by=self.faculty,
        )
        Option.objects.create(question=self.question, text="1NF", is_correct=False)
        Option.objects.create(question=self.question, text="3NF", is_correct=True)
        self.exam = Exam.objects.create(
            course=self.course,
            title="DBMS Unit Test 1",
            duration_minutes=60,
            total_marks=Decimal("50"),
            pass_mark_percent=Decimal("40"),
        )
        self.attempt = Attempt.objects.create(exam=self.exam, student=self.student)

    def set_attempt_start(self, started_at):
        Attempt.objects.filter(pk=self.attempt.pk).update(started_at=started_at)
        self.attempt.refresh_from_db()

    def test_UT_042_remaining_time_uses_server_time_for_helper_and_api(self):
        server_now = timezone.now()
        self.set_attempt_start(server_now - timedelta(minutes=10))

        self.assertEqual(remaining_seconds(self.attempt, now=server_now), 3000)
        self.client.force_login(self.student)
        response = self.client.get(
            f"/api/attempts/{self.attempt.pk}/remaining",
            HTTP_X_CLIENT_TIME="2099-01-01T00:00:00Z",
        )
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(response.json()["remaining_seconds"], 2998)
        self.assertLessEqual(response.json()["remaining_seconds"], 3000)

    def test_remaining_seconds_never_returns_a_negative_value(self):
        server_now = timezone.now()
        self.set_attempt_start(server_now - timedelta(minutes=61))
        self.assertEqual(remaining_seconds(self.attempt, now=server_now), 0)

    def test_remaining_endpoint_refuses_another_student(self):
        self.client.force_login(self.other_student)
        response = self.client.get(f"/api/attempts/{self.attempt.pk}/remaining")
        self.assertEqual(response.status_code, 403)

    def test_IT_035_student_payload_never_contains_correct_answer_data(self):
        payload = question_for_student(self.question)
        self.assertEqual(set(payload), {"id", "stem", "options"})
        self.assertEqual(set(payload["options"][0]), {"id", "text"})
        rendered = str(payload).lower()
        for forbidden_key in ("is_correct", "iscorrect", "correctoption", "answerkey"):
            self.assertNotIn(forbidden_key, rendered)

        self.client.force_login(self.student)
        response = self.client.get(f"/api/attempts/{self.attempt.pk}/remaining")
        response_text = response.content.decode().lower()
        for forbidden_key in ("is_correct", "iscorrect", "correctoption", "answerkey"):
            self.assertNotIn(forbidden_key, response_text)
