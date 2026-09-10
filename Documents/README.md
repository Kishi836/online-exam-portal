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

Four actors: **Student**, **Faculty**, **Administrator**, and the **Evaluation Engine** (a `«system»` actor that grades submissions without human involvement). Integrity monitoring is automated and
evidentiary — the system logs and flags; a human decides.

## Documentation

### In this repository (`main`)

| Document | Purpose |
|---|---|
| [`use_case_flow.md`](use_case_flow.md) | **Use case flows** — IEEE-style flow-of-events (preconditions, basic/alternate/exception flows, postconditions) for UC-1 … UC-7 |
| [`use_case_flow_diagram.png`](use_case_flow_diagram.png) | **UML use case diagram** — four actors, system boundary, `«include»` / `«extend»` relationships |
| [`user_stories.md`](user_stories.md) | **User stories** — US-01 … US-06 with acceptance criteria, grouped by actor |
| [`SRS_table.pdf`](SRS_table.pdf) | SRS requirements table |

### M1 baseline (on the [`docs/m1-deliverables`](https://github.com/Kishi836/online-exam-portal/tree/docs/m1-deliverables) branch, not yet merged to `main`)

| Document | Purpose |
|---|---|
| [`PRD_01_Online_Exam_Portal.md`](https://github.com/Kishi836/online-exam-portal/blob/docs/m1-deliverables/PRD_01_Online_Exam_Portal.md) | **Product Requirements Document** — problem, goals, tiers, requirements, NFRs, security, compliance, rollout, dependencies |
| [`M1_REQUIREMENTS.md`](https://github.com/Kishi836/online-exam-portal/blob/docs/m1-deliverables/docs/01-requirements/M1_REQUIREMENTS.md) | **M1 — Requirements Commitment.** Functional requirements, NFRs by Product/Organisational/External classification, security requirements derived by SRA, user stories by epic, RTM seed |
| [`CHANGELOG.md`](https://github.com/Kishi836/online-exam-portal/blob/docs/m1-deliverables/docs/CHANGELOG.md) | Phase-by-phase evolution log — the record of *how* the project developed, for end-of-semester presentation |

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

