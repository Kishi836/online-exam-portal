"""FR-030: the one writer of the append-only audit trail. Every creation, modification and deletion of a user,
question, examination, answer key or result calls record() in the same transaction as the change it describes.

TODO(Komal) -- call sites on main today (IT_036 needs one entry per entity class):
  user        identity/views.py register()                         record(None, "create", user)
  course      identity/views.py course_create / course_edit / course_archive
  question +  questionbank/views.py _save_question()               record(faculty, "create", question,
  answer key                                                         {"correct": <id of the correct option>})
  examination examsetup/views.py exam_create / exam_edit / exam_publish / exam_schedule
              (edit: before = snapshot(exam, FIELDS) BEFORE form.save, then changed(before, snapshot(...)) after)
  result      evaluation/engine.py evaluate()                      record(None, "evaluate", attempt,
                                                                     {"score": ..., "percentage": ..., "passed": ...})
Wrap the save and the record() in one transaction.atomic() where the view doesn't already have one.
Sites added by other Sprint 2 branches (FR-009 question edits, FR-026 publishing) call record() in those PRs."""
import json

from django.core.serializers.json import DjangoJSONEncoder

from .models import AuditEntry


def snapshot(obj, fields):
    """The current values of `fields` on `obj`, for the before/after pair of an edit."""
    return {field: getattr(obj, field) for field in fields}


def changed(before, after):
    """{field: [old, new]} for every field whose value differs."""
    return {f: [before[f], after[f]] for f in after if before.get(f) != after[f]}


def record(actor, action, obj, changes=None):
    """Append one AuditEntry and return it.

    actor   -- the signed-in user, or None when the system acts (evaluation, auto-submit). An AnonymousUser
               (e.g. a Student registering) is stored as None too.
    action  -- a short verb: "create", "update", "delete", "publish", "publish_results", "evaluate", ...
    obj     -- the affected model instance; store type(obj).__name__ as `entity` and obj.pk as `entity_id`.
    changes -- a dict; Decimal and datetime values must be turned into text first, because JSONField can't
               store them: json.loads(json.dumps(changes or {}, cls=DjangoJSONEncoder)).
    """
    # TODO(Komal): build and save the AuditEntry as described above.
    raise NotImplementedError
