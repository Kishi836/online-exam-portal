# Software Requirements Specification — Online Examination Portal

**Course:** UE23CS341A — Software Engineering, PES University, Dept. of CSE
**Project:** Online Examination System with Multiple-Choice Questions and Evaluation
**Version:** 2.0 · **Date:** 2026-09-02
**Team:** Kshitij G Shettigar (Backend & Data) · Kartik (Frontend & UX) · Komal (QA, Docs & Delivery)

---

## 1. Purpose and scope

This document specifies the functional and non-functional requirements committed for
implementation. It is a **reduced baseline**: the original M1 commitment held 83 functional and 27
non-functional requirements, which exceeded what a team of three can build and demonstrate in one
semester. This version commits **30 functional** and **10 non-functional** requirements — the
demo-critical core covering the full examination lifecycle.

Requirement identifiers are unchanged from the M1 baseline
(`docs/01-requirements/M1_REQUIREMENTS.md`) so that the PRD, this SRS, the Test Plan and the RTM all
share one identifier space. Gaps in the numbering are deliberate: a dropped requirement's ID is
retired, never reissued.

The reduction is recorded as a change request in `docs/CHANGELOG.md`.

### 1.1 Actors

| Actor | Description |
|---|---|
| **Student** | An enrolled candidate who sits examinations and views published results |
| **Faculty** | Authors questions and examinations, schedules them, publishes results |
| **Administrator** | Manages courses and reviews the audit trail |
| **System** | Automated behaviour with no human trigger — evaluation, timing, logging |

### 1.2 Out of scope

Descriptive answers and manual grading · webcam or AI proctoring · biometric identity verification ·
payments · adaptive testing · native mobile applications · offline mode · plagiarism detection.

---

## 2. Functional Requirements

Priority is **Must** for every requirement below; the Should and Could tiers of the original
baseline were dropped in their entirety by this reduction.

### 2.1 Module A — User Management & Authentication

| Req ID | Module | Requirement description | Actor | Verification method | Priority |
|---|---|---|---|---|---|
| FR-AUTH-01 | User & Auth | The system shall allow a visitor to register a Student account by submitting full name, institutional email, roll number and password. | Student | Functional test | Must |
| FR-AUTH-03 | User & Auth | The system shall authenticate a user against email and password and establish a session on success. | All | Functional test | Must |
| FR-AUTH-06 | User & Auth | The system shall assign exactly one role — Student, Faculty or Administrator — to every account, and shall restrict every screen and API endpoint to the roles authorised for it. | All | Security audit / test | Must |

### 2.2 Module B — Course & Enrollment Management

| Req ID | Module | Requirement description | Actor | Verification method | Priority |
|---|---|---|---|---|---|
| FR-CRS-01 | Course Mgmt | The system shall allow an Administrator to create, edit and archive a Course identified by course code, title and semester, and to assign one or more Faculty accounts to it. | Admin | Functional test | Must |
| FR-CRS-03 | Course Mgmt | The system shall allow Faculty or an Administrator to enroll Student accounts into a Course individually. | Faculty, Admin | Functional test | Must |
| FR-CRS-04 | Course Mgmt | The system shall permit a Student to view and attempt only those examinations that belong to Courses in which the Student is enrolled. | Student | Integration test | Must |

### 2.3 Module C — Question Bank Management

| Req ID | Module | Requirement description | Actor | Verification method | Priority |
|---|---|---|---|---|---|
| FR-QB-01 | Question Bank | The system shall allow Faculty to create a single-correct multiple-choice question consisting of a question stem, between 2 and 6 options, and exactly one option marked correct. | Faculty | Functional test | Must |
| FR-QB-04 | Question Bank | The system shall require every question to carry a Course, a topic label, a difficulty level of Easy, Medium or Hard, positive marks, and negative marks. | Faculty | Data validation test | Must |
| FR-QB-05 | Question Bank | The system shall prevent modification or deletion of a question that belongs to a published or attempted examination, and shall instead create a new version of that question. | Faculty | Database integrity test | Must |

### 2.4 Module D — Examination Authoring

| Req ID | Module | Requirement description | Actor | Verification method | Priority |
|---|---|---|---|---|---|
| FR-EX-01 | Exam Authoring | The system shall allow Faculty to create an Examination with a title, an associated Course, a duration in minutes, a declared total marks value, free-text instructions, and the per-examination policy values: negative marking (enabled/disabled and value), question and option shuffling, and the pass mark. | Faculty | Functional test | Must |
| FR-EX-02 | Exam Authoring | The system shall allow Faculty to add questions to an Examination by selecting them from the question bank. | Faculty | Functional test | Must |
| FR-EX-06 | Exam Authoring | The system shall hold an Examination in Draft state until Faculty publishes it, and shall make only published Examinations visible to Students. | Faculty | State transition test | Must |

### 2.5 Module E — Scheduling & Access Control

| Req ID | Module | Requirement description | Actor | Verification method | Priority |
|---|---|---|---|---|---|
| FR-SCH-01 | Scheduling | The system shall allow Faculty to schedule a published Examination by setting a window start date-time and a window end date-time. | Faculty | Functional test | Must |
| FR-SCH-03 | Scheduling | The system shall present to each Student a dashboard listing the Upcoming, Live and Completed Examinations of the Courses in which the Student is enrolled. | Student | Functional test | Must |
| FR-SCH-04 | Scheduling | The system shall permit a Student to begin an attempt only when the current server time lies within the examination window, the Student is enrolled, and the Student has no previously submitted attempt for that Examination. | Student | System test | Must |

### 2.6 Module F — Examination Delivery (Attempt)

| Req ID | Module | Requirement description | Actor | Verification method | Priority |
|---|---|---|---|---|---|
| FR-ATT-01 | Delivery | The system shall create an attempt record stamped with the server start time when a Student begins an Examination, and shall deliver the paper only after that record exists. | Student | Sequence test | Must |
| FR-ATT-02 | Delivery | The system shall display a countdown timer whose remaining time is derived from the server clock and the attempt start time, and shall not rely on the client clock. | Student | Security / unit test | Must |
| FR-ATT-03 | Delivery | The system shall display one question at a time together with a navigation palette showing, for every question, one of four states: Not Visited, Not Answered, Answered, or Marked for Review. | Student | UI / state test | Must |
| FR-ATT-05 | Delivery | The system shall persist every response to the server within 5 seconds of the Student selecting it, without any explicit save action by the Student. | Student | Resilience / API test | Must |
| FR-ATT-07 | Delivery | The system shall automatically submit an attempt, retaining all responses persisted up to that instant, when the remaining time reaches zero. | Student | Automation test | Must |
| FR-ATT-08 | Delivery | The system shall allow a Student whose session was interrupted to resume the same attempt, with remaining time computed from the original server start time and with all previously persisted responses restored. | Student | Fault-injection test | Must |

### 2.7 Module G — Automatic Evaluation & Scoring

| Req ID | Module | Requirement description | Actor | Verification method | Priority |
|---|---|---|---|---|---|
| FR-EVL-01 | Scoring | The system shall evaluate every submitted attempt automatically, without any human intervention. | System | Unit test | Must |
| FR-EVL-02 | Scoring | The system shall award the question's full positive marks for a correct response, shall deduct the configured negative marks for an incorrect response, and shall award zero with no deduction for a question left unattempted. | System | Calculation test | Must |
| FR-EVL-05 | Scoring | The system shall compute, for every evaluated attempt, the total score, the percentage score and a Pass or Fail outcome against the Examination's configured pass mark. | System | Calculation test | Must |

### 2.8 Module H — Results & Answer Review

| Req ID | Module | Requirement description | Actor | Verification method | Priority |
|---|---|---|---|---|---|
| FR-RES-01 | Results | The system shall withhold every evaluated result from the Student until Faculty publishes the results of that Examination. | System | Access control test | Must |
| FR-RES-02 | Results | The system shall allow Faculty to publish and to unpublish the results of an Examination. | Faculty | Functional test | Must |
| FR-RES-03 | Results | The system shall display to a Student, for a published result, the total score, the percentage, the Pass or Fail outcome and the marks obtained on each question. | Student | Functional test | Must |

### 2.9 Module I — Examination Integrity

| Req ID | Module | Requirement description | Actor | Verification method | Priority |
|---|---|---|---|---|---|
| FR-INT-01 | Integrity | The system shall record, with a server-side timestamp, every occurrence of the examination window losing focus during an active attempt. | System | Event capture test | Must |
| FR-INT-07 | Integrity | The system shall exclude all correct-answer data from every response delivered to a Student during an active attempt. | System | Payload inspection | Must |

### 2.10 Module K — Administration & Audit

| Req ID | Module | Requirement description | Actor | Verification method | Priority |
|---|---|---|---|---|---|
| FR-ADM-01 | Audit | The system shall write an append-only audit entry recording the actor, action, affected entity, timestamp and changed values for every creation, modification and deletion of a user, question, examination, answer key or result. | System | Security audit | Must |

**Functional requirement count: 30**, distributed A:3 · B:3 · C:3 · D:3 · E:3 · F:6 · G:3 · H:3 · I:2 · K:1.

---

## 3. Non-Functional Requirements

Classified as **Product**, **Organisational** and **External** per Lecture 8. Every entry states a
measure, so each is verifiable rather than aspirational.

### 3.1 Product requirements

| Req ID | Property | Requirement (measurable) | Verification method |
|---|---|---|---|
| NFR-P-01 | Speed | 95% of page loads and API responses shall complete within 2 seconds when 200 attempts are active concurrently. | Load test (JMeter / Locust), 95th-percentile response time |
| NFR-P-03 | Speed | Evaluation of a submitted 100-question attempt shall complete within 5 seconds. | Timed integration test |
| NFR-P-04 | Size / Capacity | The system shall sustain at least 200 concurrent attempts and a question bank of at least 50,000 questions without breaching NFR-P-01. | Load test with seeded bank |
| NFR-P-07 | Robustness | After an unplanned server restart, the system shall restore service within 60 seconds, and every in-progress attempt shall remain resumable with all persisted responses intact and the correct remaining time. | Fault-injection test: kill and restart during an active attempt |
| NFR-P-11 | Portability | The system shall function correctly on the two most recent versions of Chrome, Edge and Firefox on Windows, macOS and Linux, and shall remain usable at viewport widths of 360 pixels and above. | Cross-browser test matrix |

### 3.2 Organisational requirements

| Req ID | Requirement | Verification method |
|---|---|---|
| NFR-O-02 | All source code and documentation shall be held in a single Git repository; work shall proceed on feature branches; no commit shall be made directly to `main`; every merge shall be through a pull request reviewed by at least one other team member. | Git history and PR record |
| NFR-O-05 | Every functional requirement shall be linked in the Requirements Traceability Matrix to at least one test case identifier. | RTM completeness check |

### 3.3 External requirements

| Req ID | Requirement | Verification method |
|---|---|---|
| NFR-E-01 | Personal data shall be processed in accordance with the Digital Personal Data Protection Act, 2023: consent shall be obtained at registration, data shall be collected only for the stated examination purpose, and a Student's personal data shall be erasable on request within 30 days. | Privacy notice, consent record, deletion routine |
| NFR-E-03 | The system shall satisfy WCAG 2.1 Level AA: the entire attempt flow shall be operable by keyboard alone, text contrast shall be at least 4.5:1, and every option control shall carry a programmatic label for screen readers. | Automated accessibility audit + keyboard-only walkthrough |
| NFR-E-06 | Examination policy values — window, pass mark and negative marking — shall be configurable at run time and shall not be hard-coded, so that differing departmental policies can be accommodated. | Configuration review |

**Non-functional requirement count: 10** — 5 Product, 2 Organisational, 3 External.

---

## 4. Assumptions and dependencies

Students have a personal device with a supported browser and a broadband or mobile connection ·
examinations are attempted remotely, not in a supervised laboratory · server time is synchronised
via NTP, since every timing rule depends on it · a relational database is available, since scoring,
enrollment and audit are inherently relational · the system deploys on a single commodity Linux
virtual machine for the academic demonstration.

## 5. Traceability

| Artefact | Link |
|---|---|
| Product Requirements Document | `PRD_01_Online_Exam_Portal.md` |
| Original M1 baseline (83 FR / 27 NFR) | `docs/01-requirements/M1_REQUIREMENTS.md` |
| Test cases for every requirement above | `Documents/Test Plan Document.md` |
| Use case diagram | `Documents/Use Case Diagram.md` |
| Use case flow | `Documents/Use Case Flow.md` |
| Scope reduction change request | `docs/CHANGELOG.md` |

Every one of the 30 functional requirements is exercised by at least one test case in the Test Plan
Document, satisfying NFR-O-05.
