import json
from decimal import Decimal

from django.test import TestCase

from repository.models import Course, Question, Role, User


def make_user(role, email, password="Passw0rd!A", **extra):
    return User.objects.create_user(email, password, full_name=email, role=role, **extra)


class QuestionAuthoringTests(TestCase):
    def setUp(self):
        self.faculty = make_user(Role.FACULTY, "fac.a@pes.edu")
        self.other_faculty = make_user(Role.FACULTY, "fac.b@pes.edu")
        self.course = Course.objects.create(code="UE24CS351A", title="Database Management Systems", semester=5)
        self.other_course = Course.objects.create(code="UE24CS342AA5", title="Advanced Virtual Reality", semester=5)
        self.course.faculty.add(self.faculty)
        self.other_course.faculty.add(self.other_faculty)
        self.client.force_login(self.faculty)

    def question_data(self, options=None, **changes):
        options = options or [
            ("1NF", False), ("2NF", False), ("3NF", True), ("BCNF", False),
        ]
        data = {
            "course": str(self.course.pk),
            "stem": "Which normal form removes transitive dependency?",
            "topic": "Normalization",
            "difficulty": "MEDIUM",
            "positive_marks": "2",
            "negative_marks": "0.5",
            "options-TOTAL_FORMS": str(len(options)),
            "options-INITIAL_FORMS": "0",
            "options-MIN_NUM_FORMS": "0",
            "options-MAX_NUM_FORMS": "6",
        }
        for index, (text, is_correct) in enumerate(options):
            data[f"options-{index}-text"] = text
            if is_correct:
                data[f"options-{index}-is_correct"] = "on"
        return {**data, **changes}

    def test_UT_022_valid_single_correct_question_is_saved_and_listed(self):
        response = self.client.post("/faculty/questions/new/", self.question_data(), follow=True)
        question = Question.objects.get()
        self.assertEqual(question.course, self.course)
        self.assertEqual(question.options.count(), 4)
        self.assertEqual(question.options.filter(is_correct=True).count(), 1)
        self.assertContains(response, question.stem)

    def test_UT_023_one_option_is_rejected(self):
        response = self.client.post("/faculty/questions/new/", self.question_data([("3NF", True)]))
        self.assertContains(response, "A question must have between 2 and 6 options")
        self.assertFalse(Question.objects.exists())

    def test_UT_024_seven_options_are_rejected(self):
        options = [(letter, letter == "C") for letter in "ABCDEFG"]
        response = self.client.post("/faculty/questions/new/", self.question_data(options))
        self.assertContains(response, "A question must have between 2 and 6 options")
        self.assertFalse(Question.objects.exists())

    def test_UT_025_no_correct_option_is_rejected(self):
        options = [(letter, False) for letter in "ABCD"]
        response = self.client.post("/faculty/questions/new/", self.question_data(options))
        self.assertContains(response, "Exactly one option must be marked correct")

    def test_UT_026_two_correct_options_are_rejected(self):
        options = [("1NF", False), ("2NF", True), ("3NF", True), ("BCNF", False)]
        response = self.client.post("/faculty/questions/new/", self.question_data(options))
        self.assertContains(response, "Exactly one option must be marked correct")

    def test_UT_027_missing_metadata_is_rejected(self):
        for field, label in (
            ("course", "Course"), ("topic", "Topic"), ("difficulty", "Difficulty"),
            ("positive_marks", "Positive marks"), ("negative_marks", "Negative marks"),
        ):
            with self.subTest(field=field):
                response = self.client.post("/faculty/questions/new/", self.question_data(**{field: ""}))
                self.assertContains(response, "This field is required")
                self.assertFalse(Question.objects.exists())

    def test_IT_012_api_rejects_invalid_difficulty(self):
        payload = {
            "course": self.course.pk, "stem": "Question", "topic": "Normalization",
            "difficulty": "Impossible", "positive_marks": "2", "negative_marks": "0.5",
            "options": [
                {"text": "A", "is_correct": True}, {"text": "B", "is_correct": False},
            ],
        }
        response = self.client.post("/api/questions", data=json.dumps(payload), content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("Difficulty must be one of Easy, Medium or Hard", response.content.decode())

    def test_question_list_only_shows_assigned_course_questions(self):
        Question.objects.create(
            course=self.other_course, stem="Other", topic="Other", difficulty="EASY",
            positive_marks=Decimal("1"), negative_marks=Decimal("0"), created_by=self.other_faculty,
        )
        self.assertNotContains(self.client.get("/faculty/questions/"), "Other")
