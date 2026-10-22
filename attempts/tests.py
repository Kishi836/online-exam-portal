from django.test import TestCase
from django.urls import reverse

from repository.models import Course, Exam, Role, User


class StudentExamVisibilityTests(TestCase):
    def setUp(self):
        self.student = User.objects.create_user(
            email="student@example.com",
            password="testpass123",
            full_name="Test Student",
            role=Role.STUDENT,
        )

        self.other_student = User.objects.create_user(
            email="other@example.com",
            password="testpass123",
            full_name="Other Student",
            role=Role.STUDENT,
        )

        self.faculty = User.objects.create_user(
            email="faculty@example.com",
            password="testpass123",
            full_name="Test Faculty",
            role=Role.FACULTY,
        )

        self.course = Course.objects.create(
            code="CS101",
            title="Computer Science",
            semester=3,
        )
        self.course.students.add(self.student)

        self.published_exam = Exam.objects.create(
            course=self.course,
            title="Published Exam",
            duration_minutes=60,
            total_marks=100,
            pass_mark_percent=40,
            status=Exam.Status.PUBLISHED,
        )

        self.draft_exam = Exam.objects.create(
            course=self.course,
            title="Draft Exam",
            duration_minutes=60,
            total_marks=100,
            pass_mark_percent=40,
            status=Exam.Status.DRAFT,
        )

    def test_enrolled_student_sees_published_exam(self):
        self.client.force_login(self.student)

        response = self.client.get(reverse("student-exam-list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Published Exam")

    def test_unenrolled_student_does_not_see_exam(self):
        self.client.force_login(self.other_student)

        response = self.client.get(reverse("student-exam-list"))

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Published Exam")

    def test_draft_exam_is_hidden_from_list(self):
        self.client.force_login(self.student)

        response = self.client.get(reverse("student-exam-list"))

        self.assertNotContains(response, "Draft Exam")

    def test_enrolled_student_can_view_published_exam_detail(self):
        self.client.force_login(self.student)

        response = self.client.get(
            reverse(
                "student-exam-detail",
                args=[self.published_exam.pk],
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Published Exam")

    def test_unenrolled_student_cannot_view_exam_detail(self):
        self.client.force_login(self.other_student)

        response = self.client.get(
            reverse(
                "student-exam-detail",
                args=[self.published_exam.pk],
            )
        )

        self.assertEqual(response.status_code, 404)

    def test_draft_exam_detail_is_not_accessible(self):
        self.client.force_login(self.student)

        response = self.client.get(
            reverse(
                "student-exam-detail",
                args=[self.draft_exam.pk],
            )
        )

        self.assertEqual(response.status_code, 404)

    def test_faculty_cannot_access_student_exam_list(self):
        self.client.force_login(self.faculty)

        response = self.client.get(reverse("student-exam-list"))

        self.assertEqual(response.status_code, 403)
