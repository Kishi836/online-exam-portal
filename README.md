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

## 1. Candidate / Student Stories

### US-01: Timed Exam Session & Navigation

> **As a** student,
> **I want to** navigate through MCQ questions with a visible countdown timer,
> **So that** I can pace myself and submit within the allocated time window.

- **Acceptance Criteria:**
    
    - Displays a persistent countdown timer on the screen.
    - Shows a question palette indicating: _Answered_, _Unanswered_, _Marked for Review_, and _Current Question_.
    - When the timer hits `00:00`, the exam auto-locks and submits the candidate's current responses automatically.
        

### US-02: Instant Result & Score Breakdown

> **As a** student,
> **I want to** see my evaluated score and breakdown immediately after submitting (if permitted by the instructor),
> **So that** I can understand my performance without waiting days for manual grading.

- **Acceptance Criteria:**
    
    - Displays overall score, percentage, and pass/fail status immediately upon submission.
    - Provides a section-wise breakdown (e.g., Data Structures, Algorithms).
    - Hides correct answer explanations if the instructor disabled post-exam review.
## 2. Instructor / Examiner Stories

### US-03: MCQ Question Bank Management

> **As an** instructor,
> **I want to** create, categorize, and tag multiple-choice questions with single or multiple correct options,
> **So that** I can build a reusable question pool for different tests.

- **Acceptance Criteria:**
    
    - Supports creating questions with 2 to 6 options.
    - Allows marking single-correct or multi-correct answers.
    - Supports rich text, code snippets, and optional image attachments in both question prompts and answer choices.
    - Supports bulk CSV/JSON upload for rapid question ingestion.
        

### US-04: Test Configuration & Grading Rules

> **As an** instructor,
> **I want to** configure test parameters such as duration, randomized question order, and negative marking,
> **So that** I can customize difficulty and prevent answer sharing among students.

- **Acceptance Criteria:**
    
    - Configurable positive points per correct answer and negative points for incorrect answers (e.g., +4 / -1).
    - Toggle for option shuffling per candidate.
    - Toggle for partial marking on multi-select questions.
        

## 3. Evaluation Engine & System Stories

### US-05: Automated MCQ Evaluation Engine

> **As the** system,
> **I want to** evaluate candidate submissions asynchronously upon completion,
> **So that** final scores are calculated accurately and scaled without server bottlenecks.

- **Acceptance Criteria:**
    
    - Applies negative marking formulas: $\text{Total Score} = (\text{Correct} \times \text{Marks}) - (\text{Incorrect} \times \text{Penalty})$.
    - Unanswered questions award `0` points and do not trigger negative marking.
    - Evaluation job completes within $\le 2$ seconds per submission.
        

### US-06: Basic Anti-Cheating & Focus Loss Tracker

> **As an** administrator,
> **I want to** log tab switching and full-screen exits during an active exam,
> **So that** we can flag suspicious attempts for review.

- **Acceptance Criteria:**
    
    - System detects when the browser window loses focus (`visibilitychange` / `blur` events).
    - Candidate gets a warning dialog on the 1st and 2nd tab switch.
    - On the 3rd violation, the exam auto-submits or flags the attempt as "Suspicious" in the instructor dashboard.


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


