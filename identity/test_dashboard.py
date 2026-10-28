"""FR-014 -- the Student dashboard groups exams as Upcoming / Live / Completed (Test Plan UT_036-038, IT_018)."""
from datetime import timedelta
from decimal import Decimal

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from attempts.services import dashboard_groups
from repository.models import Attempt, Course, Exam, Role, User


class DashboardTests(TestCase):
    def setUp(self):
        self.student = User.objects.create_user(
            "stu.a@pesu.pes.edu", "Passw0rd!A", full_name="Stu A", role=Role.STUDENT, roll_number="PES1UG24CS001"
        )
        self.course = Course.objects.create(code="UE24CS341A", title="Software Engineering", semester=5)
        self.course.students.add(self.student)
        self.client.force_login(self.student)

    def make_exam(self, opens_in, closes_in, title="EXM_1"):
        """A published exam whose window opens and closes this far from server now."""
        now = timezone.now()
        return Exam.objects.create(
            course=self.course, title=title, duration_minutes=60, total_marks=Decimal("50"),
            pass_mark_percent=Decimal("40"), status=Exam.Status.PUBLISHED,
            window_start=now + opens_in, window_end=now + closes_in,
        )

    def test_FR_006_visible_exams_is_still_the_student_exam_list(self):
        exam = self.make_exam(timedelta(hours=-1), timedelta(hours=1))
        response = self.client.get(reverse("student-exam-list"))
        self.assertEqual(list(response.context["exams"]), [exam])

    def test_UT_036_exam_starting_tomorrow_is_upcoming_without_start_button(self):
        exam = self.make_exam(timedelta(hours=24), timedelta(hours=26))
        # TODO(Kartik): assert dashboard_groups(self.student)["upcoming"] == [exam],
        # then GET reverse("student-dashboard") and assert the start date-time is shown
        # and there is no "Start exam" button on the page.
        self.skipTest("TODO(Kartik): UT_036")

    def test_UT_037_open_window_is_live_with_start_button(self):
        exam = self.make_exam(timedelta(minutes=-10), timedelta(minutes=50))
        # TODO(Kartik): assert it is in groups["live"], and the page has a form posting to reverse("attempt-start").
        self.skipTest("TODO(Kartik): UT_037")

    def test_UT_038_submitted_exam_is_completed_without_start_button(self):
        exam = self.make_exam(timedelta(minutes=-10), timedelta(minutes=50))
        Attempt.objects.create(exam=exam, student=self.student, submitted_at=timezone.now())
        # TODO(Kartik): assert it is in groups["completed"] (not "live"), and no "Start exam" button.
        self.skipTest("TODO(Kartik): UT_038")

    def test_IT_018_classification_uses_server_time_not_client_clock(self):
        exam = self.make_exam(timedelta(hours=1), timedelta(hours=3))
        # TODO(Kartik): the client can't send a time, so a "+2 h client clock" changes nothing.
        # GET the dashboard with a spoofed header, e.g. HTTP_DATE set two hours ahead,
        # and assert the exam is still under Upcoming.
        self.skipTest("TODO(Kartik): IT_018")
