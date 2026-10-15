# Online Examination Portal

**Online examination system with multiple-choice questions and automatic evaluation.**
UE24CS341A Software Engineering mini-project, PES University.

Faculty author multiple-choice questions into a tagged question bank, assemble them into an
examination and schedule it for a fixed window. Enrolled Students attempt it under a
server-enforced timer with autosave and resume. Every submission is evaluated automatically against
the stored answer key, and results are released when Faculty publishes them.

## Team

| Member | Role |
|---|---|
| Kshitij G Shettigar | Backend & Data · repository owner |
| Kartik Basavaraj Meti | Frontend & UX |
| Komal S Sajja | QA & Documentation |

## Documents

| Document | Contents |
|---|---|
| [`Documents/SRS.pdf`](Documents/SRS.pdf) | **Software Requirements Specification** — 30 functional and 14 non-functional requirements in the course template (ID, type, description, priority, acceptance criteria, rationale), use case diagram and flows for UC-01 … UC-13 |
| [`Documents/SAD.pdf`](Documents/SAD.pdf) | **Software Architecture Document** — layered architecture and why, UML component diagram, interfaces, technology stack (Django + SQLite), deployment |
| [`Documents/Test_Plan.pdf`](Documents/Test_Plan.pdf) | **Test Plan** — 118 unit, integration and system test cases in the course template, 8–10 per use case, covering all 30 FRs |
| [`Documents/Sprint_Plan.pdf`](Documents/Sprint_Plan.pdf) | **Sprint Plan** — backlog, story points, owners, Sprint 1 (19–23 Oct) and Sprint 2 (26–30 Oct) |

## Backlog

GitHub Project **Online Exam Portal - Backlog**: one issue per SRS requirement (`FR-001` … `FR-030`,
`NFR-001` … `NFR-014`) with story points, assignee, priority and sprint.

## Workflow

Work happens on feature branches. The member who owns a backlog item raises the pull request that
closes it, another member reviews it, and only then is it merged into `main` (NFR-006).
