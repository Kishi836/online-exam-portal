# Sprint Plan — Online Examination Portal

**Course:** UE24CS341A — Software Engineering, PES University, Dept. of CSE\
**Team:** Kshitij G Shettigar (Backend & Data) · Kartik Basavaraj Meti (Frontend & UX) · Komal S Sajja (QA & Docs)\
**Version:** 1.0 · **Date:** 2026-10-15

---

## 1. Backlog

The backlog is the GitHub Project **Online Exam Portal - Backlog**, linked to this repository. It
holds **one issue per requirement in `Documents/SRS.md`** — 30 functional (`FR-001`…`FR-030`) and
14 non-functional (`NFR-001`…`NFR-014`) — each with story points, an assignee, a priority taken from
the SRS and a sprint.

**Story points** use the Fibonacci scale 1, 2, 3 (5 and 8 are reserved for items too large to
finish inside a one-week sprint; none were needed): 1 = configuration or a single check,
2 = one screen or one rule, 3 = a rule with timing, concurrency or several screens.

| Phase | Dates | Purpose |
|---|---|---|
| Backlog creation | by 12 Oct | Issues created from the SRS, story points and assignees set |
| Dry run | 12–16 Oct | Practise the workflow: branch → PR → review → merge, board automation |
| Backlog freeze | 19 Oct | Last day entries may change |
| **Sprint 1** | **19–23 Oct** | Thin end-to-end slice: Faculty sets an exam, a Student takes it, it is scored automatically |
| **Sprint 2** | **26–30 Oct** | Robust attempt, results publication, integrity and audit, NFR verification; development freeze |

## 2. Sprint 1 — 19 to 23 October

**Sprint goal:** *A Faculty member creates a course, enrolls a Student, writes questions, builds and
schedules an examination; the Student signs in, takes it under a server timer, and receives an
automatically computed score.* The one-minute Sprint 1 video records exactly this path.

| Req ID | Backlog item | Use case | Owner | Points |
|---|---|---|---|---|
| FR-001 | Student self-registration | UC-01 | Kartik | 2 |
| FR-002 | Email and password sign-in with session | UC-02 | Kartik | 2 |
| FR-003 | One role per account, enforced on every screen and endpoint | UC-02 | Kshitij | 3 |
| FR-004 | Course create / edit / archive, assign Faculty | UC-03 | Komal | 2 |
| FR-005 | Enroll Students into a Course | UC-04 | Komal | 2 |
| FR-006 | Show and allow only exams of enrolled Courses | UC-04 | Komal | 3 |
| FR-007 | Single-correct MCQ authoring (2–6 options) | UC-05 | Kartik | 3 |
| FR-008 | Mandatory question tags and marks | UC-05 | Kartik | 2 |
| FR-010 | Create an Examination with its policy values | UC-06 | Komal | 3 |
| FR-011 | Add bank questions to an Examination | UC-06 | Komal | 2 |
| FR-012 | Draft / Published examination state | UC-06 | Komal | 2 |
| FR-013 | Schedule the examination window | UC-07 | Kartik | 2 |
| FR-015 | Attempt eligibility: window, enrollment, one attempt | UC-08 | Kshitij | 3 |
| FR-016 | Server-stamped attempt record before the paper | UC-08 | Kshitij | 3 |
| FR-017 | Countdown from the server clock | UC-08 | Kartik | 3 |
| FR-020 | Automatic submission at expiry | UC-10 | Kshitij | 3 |
| FR-022 | Automatic evaluation of every submission | UC-11 | Kshitij | 3 |
| FR-023 | Positive / negative / zero marking | UC-11 | Kshitij | 2 |
| FR-029 | No correct-answer data in any Student payload | UC-13 | Kartik | 2 |
| NFR-006 | Feature branches, PR by assignee, review by another member | — | Komal | 1 |
| NFR-011 | Salted adaptive password hashing | — | Kartik | 1 |
| NFR-013 | CSRF tokens, ORM-only queries, generic error pages | — | Komal | 2 |
| NFR-014 | Secrets from environment variables, none in the repo | — | Komal | 1 |

**Sprint 1 capacity:** 52 points — Kshitij 17 · Kartik 17 · Komal 18.

**Also in Sprint 1** (course requirement, not a backlog item): Django project skeleton and a GitHub
Actions workflow that runs `python manage.py test` on every push and pull request.

## 3. Sprint 2 — 26 to 30 October

**Sprint goal:** *The attempt survives interruptions, Students see published scorecards, focus loss
and every change are recorded, and the non-functional requirements are verified.* The two-minute
Sprint 2 video shows the full lifecycle including resume, publication and the audit trail.

| Req ID | Backlog item | Use case | Owner | Points |
|---|---|---|---|---|
| FR-009 | Version a question instead of editing it once in use | UC-05 | Kshitij | 3 |
| FR-014 | Student dashboard: Upcoming / Live / Completed | UC-07 | Kartik | 2 |
| FR-018 | One question at a time with the 4-state palette | UC-08 | Kartik | 3 |
| FR-019 | Autosave every response within 5 s | UC-09 | Kshitij | 3 |
| FR-021 | Resume an interrupted attempt | UC-09 | Kshitij | 3 |
| FR-024 | Total, percentage and Pass / Fail | UC-11 | Kshitij | 2 |
| FR-025 | Withhold results until published | UC-12 | Komal | 2 |
| FR-026 | Publish and unpublish results | UC-12 | Komal | 2 |
| FR-027 | Student scorecard with per-question marks | UC-12 | Kartik | 2 |
| FR-028 | Record focus-loss events with server time | UC-13 | Kartik | 2 |
| FR-030 | Append-only audit trail | UC-13 | Komal | 3 |
| NFR-001 | 95% of requests ≤ 2 s at 200 concurrent attempts | — | Komal | 3 |
| NFR-002 | Evaluate a 100-question attempt ≤ 5 s | — | Kshitij | 1 |
| NFR-003 | 200 concurrent attempts, 50,000-question bank | — | Komal | 2 |
| NFR-004 | Service back ≤ 60 s after a restart, attempts resumable | — | Kshitij | 2 |
| NFR-005 | Chrome / Edge / Firefox, usable at 360 px | — | Kartik | 2 |
| NFR-007 | Every FR linked to a test case | — | Komal | 1 |
| NFR-008 | DPDP Act consent and erasure | — | Kartik | 2 |
| NFR-009 | WCAG 2.1 AA on the attempt flow | — | Kartik | 2 |
| NFR-010 | Policy values configurable, not hard-coded | — | Kshitij | 1 |
| NFR-012 | Lock account after 5 failed sign-ins | — | Komal | 2 |

**Sprint 2 capacity:** 45 points — Kshitij 15 · Kartik 15 · Komal 15.

## 4. How each sprint runs

| When | Event |
|---|---|
| Monday (19 Oct, 26 Oct) | **Sprint planning** — confirm the items above, split them into task sub-issues, move them to *Todo* |
| Tuesday – Thursday | Work in branches; each item's owner raises the PR that closes it (`Closes #<issue>`); another member reviews and merges |
| Daily | Short stand-up in the team group: done yesterday, doing today, blocked by |
| Friday (23 Oct, 30 Oct) | **Sprint review** — record the sprint video and upload it to `videos/`; **retrospective** notes appended to this file |

**Definition of done** for a backlog item:

1. The code is merged into `main` through a pull request raised by the item's owner and reviewed by
   another team member (NFR-006).
2. The GitHub Actions check is green on that pull request.
3. The item's test cases in `Documents/Test_Plan.md` have been executed and their *Actual Result*
   and *Test Result* columns filled in.
4. The issue is closed by the merge and its board card is in *Done*.

**Deviations.** Any departure from the SRS, SAD or Test Plan is recorded in
`Documents/Deviations.md` when it happens — what changed, why, and which requirement it affects —
for explanation at the final demo. Development is **frozen** at the end of Sprint 2 (30 Oct); after
that only documentation changes.

## 5. Retrospectives

*To be filled in at the end of each sprint.*
