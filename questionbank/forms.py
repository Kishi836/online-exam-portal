from django import forms
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet, inlineformset_factory

from repository.models import Course, Option, Question


class QuestionForm(forms.ModelForm):
    """Faculty-owned question metadata, with a course limited to their assignments."""

    difficulty = forms.ChoiceField(
        choices=Question.Difficulty.choices,
        error_messages={"invalid_choice": "Difficulty must be one of Easy, Medium or Hard"},
    )

    class Meta:
        model = Question
        fields = ("course", "stem", "topic", "difficulty", "positive_marks", "negative_marks")
        labels = {
            "course": "Course",
            "stem": "Question",
            "topic": "Topic",
            "difficulty": "Difficulty",
            "positive_marks": "Positive marks",
            "negative_marks": "Negative marks",
        }

    def __init__(self, *args, faculty, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["course"].queryset = Course.objects.filter(faculty=faculty, archived=False).order_by("code")

    def clean_positive_marks(self):
        marks = self.cleaned_data["positive_marks"]
        if marks <= 0:
            raise ValidationError("Positive marks must be greater than zero")
        return marks

    def clean_negative_marks(self):
        marks = self.cleaned_data["negative_marks"]
        if marks < 0:
            raise ValidationError("Negative marks must be zero or greater")
        return marks


class BaseOptionFormSet(BaseInlineFormSet):
    """FR-007 validation shared by HTML and API question creation."""

    def clean(self):
        super().clean()
        if any(self.errors):
            return

        options = []
        for form in self.forms:
            text = form.cleaned_data.get("text", "").strip()
            if text:
                options.append(form.cleaned_data)

        if not 2 <= len(options) <= 6:
            raise ValidationError("A question must have between 2 and 6 options")

        correct_count = sum(bool(option.get("is_correct")) for option in options)
        if correct_count != 1:
            raise ValidationError("Exactly one option must be marked correct")


OptionFormSet = inlineformset_factory(
    Question,
    Option,
    fields=("text", "is_correct"),
    formset=BaseOptionFormSet,
    extra=6,
    can_delete=False,
    max_num=6,
    validate_max=False,
)
