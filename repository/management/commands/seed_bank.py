
"""Seed a load-test question bank and exam for NFR-001 and NFR-003.

Run on a throwaway test database only:
    python manage.py seed_bank --questions 500 --students 20
    python manage.py seed_bank  # 50,000 questions, 200 students

All load-test students use STUDENT_PASSWORD, shared with locustfile.py.
"""

from datetime import timedelta
from decimal import Decimal

from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone

from repository.models import (
    Course,
    Exam,
    ExamQuestion,
    Option,
    Question,
    Role,
    User,
)

STUDENT_PASSWORD = "LoadTest!2026"
PAPER_SIZE = 25
BATCH = 2000


class Command(BaseCommand):
    help = "Seed load-test questions, students, and a fresh published exam."

    def add_arguments(self, parser):
        parser.add_argument("--questions", type=int, default=50_000)
        parser.add_argument("--students", type=int, default=200)

    @transaction.atomic
    def handle(self, *args, questions, students, **options):
        if questions < PAPER_SIZE:
            raise CommandError(f"--questions must be at least {PAPER_SIZE}.")
        if students < 1:
            raise CommandError("--students must be at least 1.")

        faculty, _ = User.objects.get_or_create(
            email="load.faculty@pes.edu",
            defaults={
                "full_name": "Load Faculty",
                "role": Role.FACULTY,
            },
        )

        course, _ = Course.objects.get_or_create(
            code="LOAD101",
            semester=5,
            defaults={"title": "Load test"},
        )
        course.faculty.add(faculty)

        # Reuse existing questions so rerunning this command does not
        # duplicate the question bank.
        existing_questions = list(
            Question.objects.filter(course=course)
            .order_by("id")[:questions]
        )

        missing_count = questions - len(existing_questions)

        if missing_count > 0:
            new_questions = Question.objects.bulk_create(
                [
                    Question(
                        course=course,
                        stem=f"Load question {i}",
                        topic=f"Topic {i % 50}",
                        difficulty=Question.Difficulty.MEDIUM,
                        positive_marks=Decimal("2"),
                        negative_marks=Decimal("0.5"),
                        created_by=faculty,
                    )
                    for i in range(
                        len(existing_questions),
                        questions,
                    )
                ],
                batch_size=BATCH,
            )
            existing_questions.extend(new_questions)

        bank = existing_questions[:questions]
        self.stdout.write(f"{len(bank)} questions ready")

        # Ensure every seeded question has four options.
        # Reuse questions that already have options.
        all_options = []
        for question in bank:
            existing_options = Option.objects.filter(
                question=question
            ).count()

            if existing_options == 0:
                all_options.extend(
                    [
                        Option(
                            question=question,
                            text=f"Correct answer for {question.stem}",
                            is_correct=True,
                        ),
                        Option(
                            question=question,
                            text=f"Wrong answer A for {question.stem}",
                            is_correct=False,
                        ),
                        Option(
                            question=question,
                            text=f"Wrong answer B for {question.stem}",
                            is_correct=False,
                        ),
                        Option(
                            question=question,
                            text=f"Wrong answer C for {question.stem}",
                            is_correct=False,
                        ),
                    ]
                )

        if all_options:
            Option.objects.bulk_create(
                all_options,
                batch_size=BATCH,
            )

        self.stdout.write(
            f"{len(all_options)} new options created"
        )

        # Reuse existing load-test users; create only missing users.
        password_hash = make_password(STUDENT_PASSWORD)
        the_students = []

        for i in range(1, students + 1):
            email = f"load.student{i}@pesu.pes.edu"
            roll_number = f"LOAD{i:04d}"

            student, created = User.objects.get_or_create(
                email=email,
                defaults={
                    "password": password_hash,
                    "full_name": f"Load Student {i}",
                    "roll_number": roll_number,
                    "role": Role.STUDENT,
                },
            )

            if created:
                the_students.append(student)
            elif student.role != Role.STUDENT:
                raise CommandError(
                    f"{email} exists but is not a Student account."
                )

            course.students.add(student)

        self.stdout.write(
            f"{students} load-test students ready and enrolled"
        )

        # Every run gets a fresh exam so submitted attempts from previous
        # smoke tests do not prevent the same students from testing again.
        now = timezone.now()
        exam = Exam.objects.create(
            course=course,
            title=f"Load Test Exam {now:%Y%m%d-%H%M%S}",
            duration_minutes=60,
            total_marks=PAPER_SIZE * 2,
            pass_mark_percent=40,
            status=Exam.Status.PUBLISHED,
            published_at=now,
            window_start=now - timedelta(hours=1),
            window_end=now + timedelta(hours=3),
        )

        ExamQuestion.objects.bulk_create(
            [
                ExamQuestion(
                    exam=exam,
                    question=question,
                    order=i,
                )
                for i, question in enumerate(
                    bank[:PAPER_SIZE],
                    start=1,
                )
            ],
            batch_size=BATCH,
        )

        self.stdout.write(
            self.style.SUCCESS(f"Exam ID: {exam.pk}")
        )
