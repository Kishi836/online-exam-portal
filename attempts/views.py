
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_GET

from identity.access import roles
from repository.models import Exam, Role


@roles(Role.STUDENT)
@require_GET
def student_exam_list(request):
    exams = (
        Exam.objects.filter(
            course__students=request.user,
            status=Exam.Status.PUBLISHED,
        )
        .select_related("course")
        .order_by("title")
    )

    return render(
        request,
        "attempts/student_exam_list.html",
        {"exams": exams},
    )


@roles(Role.STUDENT)
@require_GET
def student_exam_detail(request, exam_id):
    exam = get_object_or_404(
        Exam.objects.select_related("course").filter(
            course__students=request.user,
            status=Exam.Status.PUBLISHED,
        ),
        pk=exam_id,
    )

    return render(
        request,
        "attempts/student_exam_detail.html",
        {"exam": exam},
    )
