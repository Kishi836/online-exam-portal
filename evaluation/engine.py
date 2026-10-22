"""Evaluation Engine (SAD 3.1): IEvaluation, called by the Attempt Session Manager on submission."""
from decimal import Decimal


def marks_for(question, option, negative_marking):
    """FR-023: full positive marks if correct, minus the configured negative marks if wrong, zero if unanswered."""
    if option is None:
        return Decimal("0")
    if option.is_correct:
        return question.positive_marks
    return -question.negative_marks if negative_marking else Decimal("0")


def evaluate(attempt):
    """FR-022: score the attempt and store it. A question with no Answer row is unanswered and adds nothing."""
    negative_marking = attempt.exam.negative_marking
    attempt.score = sum(
        (marks_for(a.question, a.option, negative_marking) for a in attempt.answers.select_related("question", "option")),
        Decimal("0"),
    )
    attempt.save(update_fields=["score"])
    return attempt.score
