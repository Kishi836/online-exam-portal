"""Results (SAD 3.1): business operations on published results. The visibility rule is attempts.services.result_visible."""


def scorecard(attempt):
    """FR-027: everything the Student's scorecard shows, read from the stored evaluation -- nothing is re-scored.

    Returns {"score", "total_marks", "percentage", "passed", "rows"} where rows is one dict per question
    in paper order: {"n", "stem", "chosen" (option text or None), "marks" (Decimal, 0 when unanswered)}.
    Every question on the paper gets a row, answered or not (UT_062: all 25 lines).
    """
    answers = {a.question_id: a for a in attempt.answers.select_related("option")}
    rows = []
    for n, question in enumerate(attempt.exam.questions.order_by("examquestion__order"), start=1):
        answer = answers.get(question.id)
        # TODO(Kartik): append the row. `marks` comes from answer.marks (set by the evaluation engine);
        # a question with no Answer row, or an Answer with no option, is unanswered -> Decimal("0").
        # Never include Option.is_correct or the correct option's text (FR-029 spirit; the SRS asks only for marks).
    # TODO(Kartik): return the dict, taking score / percentage / passed straight from `attempt`.
    raise NotImplementedError
