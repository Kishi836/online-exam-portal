"""NFR-001, NFR-003: seed a load-test database -- a 50,000-question bank and one live exam for 200 Students.

    python manage.py seed_bank                      # 50,000 questions, 200 students
    python manage.py seed_bank --questions 500      # a quick run while you work

Run it on a throwaway database only, never on one with real data. Students are
load.student<N>@pesu.pes.edu, all with the password in STUDENT_PASSWORD, so locustfile.py can sign them in.
"""
from datetime import timedelta
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from repository.models import Course, Exam, ExamQuestion, Option, Question, Role, User

STUDENT_PASSWORD = "LoadTest!2026"
PAPER_SIZE = 25
BATCH = 2000


class Command(BaseCommand):
    help = "Seed a 50,000-question bank and one live exam for 200 students (NFR-001, NFR-003)."

    def add_arguments(self, parser):
        parser.add_argument("--questions", type=int, default=50_000)
        parser.add_argument("--students", type=int, default=200)

    @transaction.atomic
    def handle(self, *args, questions, students, **options):
        faculty, _ = User.objects.get_or_create(
            email="load.faculty@pes.edu", defaults={"full_name": "Load Faculty", "role": Role.FACULTY}
        )
        course, _ = Course.objects.get_or_create(code="LOAD101", semester=5, defaults={"title": "Load test"})
        course.faculty.add(faculty)

        bank = Question.objects.bulk_create(
            (
                Question(
                    course=course, stem=f"Load question {i}", topic=f"Topic {i % 50}",
                    difficulty=Question.Difficulty.MEDIUM, positive_marks=Decimal("2"),
                    negative_marks=Decimal("0.5"), created_by=faculty,
                )
                for i in range(questions)
            ),
            batch_size=BATCH,
        )
        self.stdout.write(f"{len(bank)} questions")

        # TODO(Komal): 4 options per question in `bank`, exactly one with is_correct=True.
        # Build them all in one list and call Option.objects.bulk_create(..., batch_size=BATCH) once.

        # TODO(Komal): `students` Student users load.student1@pesu.pes.edu ... with roll numbers LOAD0001 ...
        # create_user hashes every password (slow, about 0.3 s each). Instead, hash STUDENT_PASSWORD once with
        # django.contrib.auth.hashers.make_password, set password=<that hash> on each User(...), then
        # bulk_create them. Then enrol them all: course.students.add(*the_students).

        # TODO(Komal): one exam on `course` that is open right now:
        #   status=Exam.Status.PUBLISHED, published_at=timezone.now(),
        #   window_start=now - 1 hour, window_end=now + 3 hours, duration_minutes=60,
        #   total_marks = PAPER_SIZE * 2, pass_mark_percent=40.
        # Attach the first PAPER_SIZE questions of `bank` with ExamQuestion(exam=..., question=..., order=i).
        # Print the exam's id at the end. locustfile.py needs it (LOAD_EXAM_ID).
