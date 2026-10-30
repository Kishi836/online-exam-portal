"""NFR-008 (DPDP Act 2023): erase a Student's personal data on request.

Erasure anonymises the account in place instead of deleting it: Attempt and Answer rows PROTECT their
Student, and the examination record (scores, audit) must survive without saying who sat it.
"""
from django.db import transaction

from repository.models import Role


class NotAStudent(Exception):
    """Only Student accounts are erased; Faculty and Admin accounts are institutional."""


def erase_student(student):
    """Replace every personal field with a placeholder and disable sign-in. Attempts are kept, anonymised.

    After this: full_name "Erased student", email f"erased-{pk}@invalid.local", roll_number None,
    consent_given_at None, an unusable password, is_active False.
    """
    if student.role != Role.STUDENT:
        raise NotAStudent("Only Student accounts can be erased")
    with transaction.atomic():
        # TODO(Kartik): set the fields above, student.set_unusable_password(), student.save().
        # Also log the Student out everywhere: delete their sessions
        # (django.contrib.sessions.models.Session rows whose get_decoded().get("_auth_user_id") == str(pk)).
        raise NotImplementedError
