def question_for_student(question):
    """FR-029: the only question shape allowed in a Student-facing response."""
    return {
        "id": question.id,
        "stem": question.stem,
        "options": list(question.options.values("id", "text")),
    }
