"""Evaluation Engine (SAD 3.1): IEvaluation, called by the Attempt Session Manager on submission."""
from decimal import ROUND_HALF_UP, Decimal


def marks_for(question, option, negative_marking):
    """FR-023: full positive marks if correct, minus the configured negative marks if wrong, zero if unanswered."""
    if option is None:
        return Decimal("0")
    if option.is_correct:
        return question.positive_marks
    return -question.negative_marks if negative_marking else Decimal("0")


def outcome(score, total_marks, pass_mark_percent):
    """FR-024: (percentage to 2 places, passed). The pass mark is inclusive (SRS open question 2).

    Pass/Fail compares the exact score, so rounding the stored percentage can never flip it.
    A non-positive declared total has no percentage; the outcome is then unknown, not Fail.
    """
    if total_marks <= 0:
        return None, None
    percentage = (score * 100 / total_marks).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    return percentage, score * 100 >= pass_mark_percent * total_marks


def evaluate(attempt):
    """FR-022: score the attempt and store it. A question with no Answer row is unanswered and adds nothing."""
    exam = attempt.exam
    attempt.score = sum(
        (marks_for(a.question, a.option, exam.negative_marking) for a in attempt.answers.select_related("question", "option")),
        Decimal("0"),
    )
    # NFR-010: the pass mark comes from the exam, never from code.
    attempt.percentage, attempt.passed = outcome(attempt.score, exam.total_marks, exam.pass_mark_percent)
    attempt.save(update_fields=["score", "percentage", "passed"])
    return attempt.score
