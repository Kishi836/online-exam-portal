# Online Examination Portal

**Online examination system with multiple-choice questions and evaluation.**


---

## What it does

Faculty author multiple-choice questions into a reusable, tagged question bank, assemble papers from
it either by hand or automatically, and schedule them for a fixed window. Enrolled students attempt
the paper under a server-enforced timer with autosave and resume-after-disconnection. Every
submission is **evaluated automatically** against the stored answer key — no manual grading — and
results are published at the faculty's discretion with per-question scorecards and cohort
statistics.

Three actors: **Student**, **Faculty**, **Administrator**. Integrity monitoring is automated and
evidentiary — the system logs and flags; a human decides.

## Documentation

| Document | Purpose |
|---|---|
| [`PRD_01_Online_Exam_Portal.md`](PRD_01_Online_Exam_Portal.md) | **Product Requirements Document** — source of truth. Problem, goals, tiers, 79 requirements, NFRs, security, compliance, rollout, dependencies |
| [`docs/01-requirements/M1_REQUIREMENTS.md`](docs/01-requirements/M1_REQUIREMENTS.md) | **M1 — Requirements Commitment.** The formally specified subset committed for this semester: 74 functional requirements, NFRs by Product/Organisational/External classification, security requirements derived by SRA, 36 user stories across 8 epics, RTM seed |
| [`docs/CHANGELOG.md`](docs/CHANGELOG.md) | Phase-by-phase evolution log — the record of *how* the project developed, for end-of-semester presentation |

## Milestones

| Milestone | Deliverable | Status |
|---|---|---|
| **M1** | Requirements commitment: FRs, NFRs, security requirements, user stories, product backlog | ✅ Baselined |
| **M2** | SRS (IEEE Std 830-1998), UML use-case and class diagrams, architecture, stack decision | ⬜ Sprint 1 |
| **M3** | Design documents, ERD, sequence diagrams, working increment of Epics 1–4 | ⬜ Sprints 2–3 |
| **M4** | Working increment of Epics 5–8, test plan, executed test cases, completed RTM | ⬜ Sprint 4 |
| **M5** | Final demonstration, deployment, retrospective | ⬜ End of semester |

## Scope at a glance

**In:** role-based accounts · courses and enrollment · MCQ/MSQ/True-False question bank with topic
and difficulty tagging · manual and auto-generated paper assembly · scheduled windows ·
server-timed delivery with autosave, palette navigation, resume and auto-submit · deterministic
automatic evaluation with configurable negative marking · post-hoc answer-key correction with bulk
re-evaluation · scorecards, answer review and cohort statistics · integrity event logging ·
append-only audit trail · CSV export.

**Out:** descriptive answers and manual grading · webcam or AI proctoring · biometric identity
verification · payments · adaptive testing · native mobile apps · offline mode · plagiarism
detection.

## Working agreements

- Feature branches only — no direct commits to `main`; every merge through a reviewed pull request.
- Each sprint ends with a tagged, demonstrable increment.
- The RTM is updated at every phase; every Must-priority requirement links to at least one test case.
- Changes to a baselined requirement go through change control and are recorded in the changelog.

## Team

| Member | Role |
|---|---|
| **Kshitij** (repo owner) | Backend & data lead |
| **Kartik** | Frontend & UX lead |
| **Komal** | QA, docs & delivery lead |

All three review every pull request; sprint ceremonies and the final viva are shared.
