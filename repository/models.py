"""Exam Repository (SAD 3.1): the Data layer. Every Business app reads and writes through these models."""
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class Role(models.TextChoices):
    STUDENT = "STUDENT", "Student"
    FACULTY = "FACULTY", "Faculty"
    ADMIN = "ADMIN", "Administrator"


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **fields):
        user = self.model(email=self.normalize_email(email), **fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **fields):
        fields.update(role=Role.ADMIN, is_staff=True, is_superuser=True)
        return self.create_user(email, password, **fields)


class User(AbstractUser):
    """Signs in with email. FR-003: exactly one role -- a single required field the database checks."""

    username = None
    first_name = None
    last_name = None
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=150)
    roll_number = models.CharField(
        max_length=20, unique=True, null=True, blank=True)  # Students only
    role = models.CharField(max_length=7, choices=Role.choices)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name"]
    objects = UserManager()

    class Meta:
        constraints = [
            models.CheckConstraint(condition=models.Q(
                role__in=Role.values), name="user_has_one_valid_role"),
        ]

    def get_full_name(self):
        return self.full_name

    def get_short_name(self):
        return self.full_name


class Course(models.Model):
    code = models.CharField(max_length=20)
    title = models.CharField(max_length=200)
    semester = models.PositiveSmallIntegerField()
    archived = models.BooleanField(default=False)
    faculty = models.ManyToManyField(
        User, related_name="taught_courses", limit_choices_to={"role": Role.FACULTY})

    # FR-005: Faculty or Administrator can enroll and unenroll Students in a Course.
    students = models.ManyToManyField(
        User,
        related_name="enrolled_courses",
        blank=True,
        limit_choices_to={"role": Role.STUDENT},
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["code", "semester"],
                name="course_code_unique_per_semester",
            )
        ]

    def __str__(self):
        return f"{self.code} {self.title}"


class Question(models.Model):
    class Difficulty(models.TextChoices):
        EASY = "EASY", "Easy"
        MEDIUM = "MEDIUM", "Medium"
        HARD = "HARD", "Hard"

    course = models.ForeignKey(
        Course, on_delete=models.PROTECT, related_name="questions")
    stem = models.TextField()
    topic = models.CharField(max_length=100)
    difficulty = models.CharField(max_length=6, choices=Difficulty.choices)
    positive_marks = models.DecimalField(max_digits=5, decimal_places=2)
    negative_marks = models.DecimalField(
        max_digits=5, decimal_places=2, default=0)
    created_by = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="questions")

    def __str__(self):
        return self.stem[:60]


class Option(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="options")
    text = models.TextField()
    # FR-029: never part of anything sent to a Student
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text[:60]


class Exam(models.Model):
    class Status(models.TextChoices):
        DRAFT = "DRAFT", "Draft"
        PUBLISHED = "PUBLISHED", "Published"

    course = models.ForeignKey(
        Course, on_delete=models.PROTECT, related_name="exams")
    title = models.CharField(max_length=200)
    duration_minutes = models.PositiveIntegerField()
    total_marks = models.DecimalField(max_digits=6, decimal_places=2)
    instructions = models.TextField(blank=True)
    # the deduction itself is Question.negative_marks
    negative_marking = models.BooleanField(default=True)
    shuffle_questions = models.BooleanField(default=False)
    shuffle_options = models.BooleanField(default=False)
    pass_mark_percent = models.DecimalField(max_digits=5, decimal_places=2)
    status = models.CharField(
        max_length=9, choices=Status.choices, default=Status.DRAFT)
    window_start = models.DateTimeField(null=True, blank=True)
    window_end = models.DateTimeField(null=True, blank=True)
    questions = models.ManyToManyField(
        Question, through="ExamQuestion", related_name="exams")

    def __str__(self):
        return self.title


class ExamQuestion(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.PROTECT)
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ["order"]
        constraints = [models.UniqueConstraint(
            fields=["exam", "question"], name="question_once_per_exam")]


class Attempt(models.Model):
    exam = models.ForeignKey(
        Exam, on_delete=models.PROTECT, related_name="attempts")
    student = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="attempts")
    # FR-016: the server's clock, never the client's
    started_at = models.DateTimeField(auto_now_add=True)
    submitted_at = models.DateTimeField(null=True, blank=True)
    score = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True)

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=["exam", "student"], name="one_attempt_per_student")]


class Answer(models.Model):
    attempt = models.ForeignKey(
        Attempt, on_delete=models.CASCADE, related_name="answers")
    question = models.ForeignKey(Question, on_delete=models.PROTECT)
    option = models.ForeignKey(
        Option, on_delete=models.PROTECT, null=True, blank=True)  # null = unanswered
    saved_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=["attempt", "question"], name="one_answer_per_question")]
