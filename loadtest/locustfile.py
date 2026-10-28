"""NFR-001 / NFR-003 load test: 200 Students sign in, start the live exam, answer, and submit.

Locust is NOT in requirements.txt. Install it in your own venv: pip install locust

    python manage.py seed_bank                                # prints the exam id
    $env:LOAD_EXAM_ID = "<that id>"
    python manage.py runserver --insecure                     # DEBUG off (the default)
    locust -f loadtest/locustfile.py --host http://127.0.0.1:8000 --headless -u 200 -r 20 -t 5m --html loadtest/report.html

Pass: the 95th percentile of every request is 2 s or less (NFR-001), with the 50,000-question bank seeded (NFR-003).
The report goes in the PR description, not in git (loadtest/report*.html is ignored).
"""
import itertools
import os
import re

from locust import HttpUser, between, task

EXAM_ID = os.environ.get("LOAD_EXAM_ID", "1")
PASSWORD = "LoadTest!2026"  # same as seed_bank.STUDENT_PASSWORD
student_numbers = itertools.count(1)


class Student(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        """Each simulated user is a different seeded Student: load.student1, load.student2, ..."""
        self.email = f"load.student{next(student_numbers)}@pesu.pes.edu"
        self.attempt_url = None
        # TODO(Komal): sign in.
        #  1. GET /login/ and read the csrftoken cookie: self.client.cookies.get("csrftoken")
        #  2. POST /login/ with {"email": ..., "password": PASSWORD, "csrfmiddlewaretoken": token}
        # Then start the exam:
        #  3. POST /api/attempts with {"exam": EXAM_ID, "csrfmiddlewaretoken": token}. It redirects to /attempts/<id>/.
        #     Keep that path in self.attempt_url (the final response.url), and the paper HTML for answer().

    @task(5)
    def answer(self):
        # TODO(Komal): POST f"/api/attempts/<id>/answers" with question and option ids taken from the paper HTML
        # (the radio inputs: data-question="..." value="..."; re.findall is enough), the X-CSRFToken header,
        # and name="answer" so all saves are grouped in one row of the report.
        pass

    @task(1)
    def check_timer(self):
        # TODO(Komal): GET f"/api/attempts/<id>/remaining" with name="remaining".
        pass

    def on_stop(self):
        # TODO(Komal): POST f"{self.attempt_url}submit" with the CSRF token, so every attempt ends submitted.
        pass
