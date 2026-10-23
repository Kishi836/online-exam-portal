
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.db.models import Max
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_GET, require_POST

from identity.access import roles
from repository.models import Exam, ExamQuestion, Role

from .forms import ExamForm, ExamQuestionForm


def _faculty_exam_or_403(request, exam_id):
    exam = get_object_or_404(
        Exam.objects.select_related("course"), pk=exam_id
    )
    if not exam.course.faculty.filter(pk=request.user.pk).exists():
        raise PermissionDenied("You are not assigned to this course.")
    return exam


@roles(Role.FACULTY)
@require_GET
def exam_list(request):
    exams = (
        Exam.objects.filter(course__faculty=request.user)
        .select_related("course")
        .order_by("-id")
    )
    return render(
        request, "examsetup/exam_list.html", {"exams": exams}
    )


@roles(Role.FACULTY)
def exam_create(request):
    if request.method == "POST":
        form = ExamForm(request.POST, user=request.user)
        if form.is_valid():
            exam = form.save(commit=False)
            if exam.course.archived:
                form.add_error("course", "This course is archived")
            else:
                exam.status = Exam.Status.DRAFT
                exam.published_at = None
                exam.save()
                messages.success(request, "Exam created as Draft.")
                return redirect("exam-detail", exam_id=exam.pk)
    else:
        form = ExamForm(user=request.user)

    return render(
        request,
        "examsetup/exam_form.html",
        {"form": form, "heading": "Create exam"},
    )


@roles(Role.FACULTY)
def exam_edit(request, exam_id):
    exam = _faculty_exam_or_403(request, exam_id)
    if exam.status != Exam.Status.DRAFT:
        raise PermissionDenied("Only Draft exams can be edited.")

    if request.method == "POST":
        form = ExamForm(
            request.POST, instance=exam, user=request.user
        )
        if form.is_valid():
            updated = form.save(commit=False)
            if updated.course.archived:
                form.add_error("course", "This course is archived")
            else:
                updated.save()
                messages.success(request, "Draft exam updated.")
                return redirect("exam-detail", exam_id=exam.pk)
    else:
        form = ExamForm(instance=exam, user=request.user)

    return render(
        request,
        "examsetup/exam_form.html",
        {"form": form, "heading": "Edit draft exam"},
    )


@roles(Role.FACULTY)
@require_GET
def exam_detail(request, exam_id):
    exam = _faculty_exam_or_403(request, exam_id)
    exam_questions = (
        exam.examquestion_set.select_related("question")
        .order_by("order")
    )
    return render(
        request,
        "examsetup/exam_detail.html",
        {"exam": exam, "exam_questions": exam_questions},
    )


@roles(Role.FACULTY)
def exam_add_questions(request, exam_id):
    exam = _faculty_exam_or_403(request, exam_id)

    if exam.status != Exam.Status.DRAFT:
        raise PermissionDenied(
            "Only Draft exams can have questions added."
        )
    if exam.course.archived:
        raise PermissionDenied("This course is archived")

    if request.method == "POST":
        form = ExamQuestionForm(request.POST, exam=exam)
        if form.is_valid():
            max_order = (
                ExamQuestion.objects.filter(exam=exam)
                .aggregate(max_order=Max("order"))["max_order"]
            )
            next_order = 0 if max_order is None else max_order + 1

            for question in form.cleaned_data["questions"]:
                ExamQuestion.objects.create(
                    exam=exam,
                    question=question,
                    order=next_order,
                )
                next_order += 1

            messages.success(request, "Questions added.")
            return redirect("exam-detail", exam_id=exam.pk)
    else:
        form = ExamQuestionForm(exam=exam)

    return render(
        request,
        "examsetup/exam_questions.html",
        {"form": form, "exam": exam},
    )


@roles(Role.FACULTY)
@require_POST
def exam_publish(request, exam_id):
    exam = _faculty_exam_or_403(request, exam_id)

    if exam.status != Exam.Status.DRAFT:
        raise PermissionDenied(
            "Only Draft exams can be published."
        )
    if exam.course.archived:
        raise PermissionDenied("This course is archived")
    if not ExamQuestion.objects.filter(exam=exam).exists():
        messages.error(
            request, "Add at least one question before publishing."
        )
        return redirect("exam-detail", exam_id=exam.pk)

    exam.status = Exam.Status.PUBLISHED
    exam.published_at = timezone.now()
    exam.save(update_fields=["status", "published_at"])

    messages.success(request, "Exam published.")
    return redirect("exam-detail", exam_id=exam.pk)
