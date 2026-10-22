from django import forms
from django.core.exceptions import ValidationError

from .models import Course, Role, User


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ["code", "title", "semester", "faculty"]
        widgets = {
            "faculty": forms.CheckboxSelectMultiple(),
        }

    def clean_title(self):
        title = self.cleaned_data.get("title", "").strip()
        if not title:
            raise ValidationError("Course title is required")
        return title

    def clean(self):
        cleaned_data = super().clean()
        code = cleaned_data.get("code")
        semester = cleaned_data.get("semester")

        if code and semester is not None:
            existing = Course.objects.filter(
                code=code,
                semester=semester,
            )
            if self.instance.pk:
                existing = existing.exclude(pk=self.instance.pk)

            if existing.exists():
                raise ValidationError(
                    "A course with this code already exists for the selected semester"
                )

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title"].required = False
        self.fields["faculty"].queryset = User.objects.filter(
            role=Role.FACULTY
        )


class EnrollmentForm(forms.Form):
    student = forms.ModelChoiceField(
        queryset=User.objects.none(),
        label="Student",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["student"].queryset = User.objects.filter(
            role=Role.STUDENT
        )
