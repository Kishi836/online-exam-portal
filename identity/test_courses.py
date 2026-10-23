
from django.test import TestCase

from repository.models import Course, Role, User


def make_user(role, email, **extra):
    return User.objects.create_user(
        email,
        "Passw0rd!A",
        full_name=email,
        role=role,
        **extra,
    )


class CourseTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin = make_user(Role.ADMIN, "admin@pes.edu")
        cls.fac_a = make_user(Role.FACULTY, "fac.a@pes.edu")
        cls.fac_b = make_user(Role.FACULTY, "fac.b@pes.edu")
        cls.student = make_user(
            Role.STUDENT,
            "stu.a@pesu.pes.edu",
            roll_number="PES1UG24CS001",
        )

    def test_IT_009_admin_can_enroll_a_student(self):
        course = self.make_course()
        self.client.force_login(self.admin)

        response = self.client.post(
            f"/courses/{course.pk}/enroll/",
            {"student": self.student.pk},
            follow=True,
        )

        self.assertTrue(
            course.students.filter(pk=self.student.pk).exists()
        )
        self.assertContains(response, self.student.email)

    def make_course(self, code="UE24CS351A", semester=5):
        course = Course.objects.create(
            code=code,
            title="Database Management Systems",
            semester=semester,
        )
        course.faculty.add(self.fac_a)
        return course

    def test_UT_012_admin_creates_a_course(self):
        self.client.force_login(self.admin)

        response = self.client.post(
            "/admin/courses/new/",
            {
                "code": "UE24CS351A",
                "title": "Database Management Systems",
                "semester": 5,
                "faculty": [self.fac_a.pk],
            },
            follow=True,
        )

        self.assertTrue(
            Course.objects.filter(
                code="UE24CS351A",
                semester=5,
                title="Database Management Systems",
            ).exists()
        )
        self.assertContains(response, "UE24CS351A")
        self.assertTrue(
            Course.objects.get(code="UE24CS351A").faculty.filter(
                pk=self.fac_a.pk
            ).exists()
        )

    def test_UT_013_empty_course_title_is_rejected(self):
        self.client.force_login(self.admin)

        response = self.client.post(
            "/admin/courses/new/",
            {
                "code": "UE24CS999A",
                "title": "",
                "semester": 5,
                "faculty": [self.fac_a.pk],
            },
        )

        self.assertContains(response, "Course title is required")
        self.assertFalse(Course.objects.filter(code="UE24CS999A").exists())

    def test_UT_014_duplicate_code_and_semester_is_rejected(self):
        self.make_course()
        self.client.force_login(self.admin)

        response = self.client.post(
            "/admin/courses/new/",
            {
                "code": "UE24CS351A",
                "title": "DBMS Repeat",
                "semester": 5,
                "faculty": [self.fac_a.pk],
            },
        )

        self.assertContains(
            response,
            "A course with this code already exists for the selected semester",
        )
        self.assertEqual(
            Course.objects.filter(code="UE24CS351A", semester=5).count(),
            1,
        )

    def test_UT_015_student_cannot_be_assigned_as_faculty(self):
        self.client.force_login(self.admin)

        response = self.client.post(
            "/admin/courses/new/",
            {
                "code": "UE24CS352A",
                "title": "Networks",
                "semester": 5,
                "faculty": [self.student.pk],
            },
        )

        self.assertFalse(Course.objects.filter(code="UE24CS352A").exists())

    def test_UT_016_assigning_same_faculty_twice_has_one_assignment(self):
        course = self.make_course()
        course.faculty.add(self.fac_a, self.fac_a)

        self.assertEqual(
            course.faculty.filter(pk=self.fac_a.pk).count(),
            1,
        )

    def test_UT_017_faculty_can_enroll_a_student(self):
        course = self.make_course()
        self.client.force_login(self.fac_a)

        response = self.client.post(
            f"/courses/{course.pk}/enroll/",
            {"student": self.student.pk},
            follow=True,
        )

        self.assertTrue(course.students.filter(pk=self.student.pk).exists())
        self.assertContains(response, self.student.email)

    def test_UT_018_duplicate_enrollment_is_rejected(self):
        course = self.make_course()
        course.students.add(self.student)
        self.client.force_login(self.fac_a)

        response = self.client.post(
            f"/courses/{course.pk}/enroll/",
            {"student": self.student.pk},
        )

        self.assertContains(response, "This student is already enrolled")
        self.assertEqual(course.students.filter(pk=self.student.pk).count(), 1)

    def test_UT_019_faculty_account_cannot_be_enrolled_as_student(self):
        course = self.make_course()
        self.client.force_login(self.fac_a)

        response = self.client.post(
            f"/courses/{course.pk}/enroll/",
            {"student": self.fac_b.pk},
        )

        self.assertFalse(course.students.filter(pk=self.fac_b.pk).exists())
        self.assertEqual(response.status_code, 200)

    def test_UT_020_unassigned_faculty_cannot_enroll_students(self):
        course = self.make_course()
        self.client.force_login(self.fac_b)

        response = self.client.post(
            f"/courses/{course.pk}/enroll/",
            {"student": self.student.pk},
        )

        self.assertEqual(response.status_code, 403)
        self.assertFalse(course.students.filter(pk=self.student.pk).exists())

    def test_IT_007_archived_course_rejects_enrollment(self):
        course = self.make_course()
        course.archived = True
        course.save(update_fields=["archived"])
        self.client.force_login(self.fac_a)

        response = self.client.post(
            f"/courses/{course.pk}/enroll/",
            {"student": self.student.pk},
            follow=True,
        )

        self.assertContains(response, "This course is archived")
        self.assertFalse(course.students.filter(pk=self.student.pk).exists())

    def test_IT_008_newly_assigned_faculty_sees_course(self):
        course = self.make_course()
        course.faculty.add(self.fac_b)
        self.client.force_login(self.fac_b)

        response = self.client.get("/faculty/courses/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, course.code)

    def test_ST_003_admin_creates_and_archives_course(self):
        self.client.force_login(self.admin)

        response = self.client.post(
            "/admin/courses/new/",
            {
                "code": "UE24CS360A",
                "title": "Operating Systems",
                "semester": 5,
                "faculty": [self.fac_a.pk],
            },
            follow=True,
        )

        course = Course.objects.get(code="UE24CS360A", semester=5)
        self.assertTrue(course.faculty.filter(pk=self.fac_a.pk).exists())
        self.assertContains(response, "UE24CS360A")

        response = self.client.post(
            f"/admin/courses/{course.pk}/archive/",
            follow=True,
        )

        course.refresh_from_db()
        self.assertTrue(course.archived)
