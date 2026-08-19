# M1 — Requirements Commitment
## Online Examination System with Multiple-Choice Questions and Evaluation

> **Course:** UE23CS341A — Software Engineering (Unit 1, Requirements Engineering)
> **Assignment:** Jackfruit (semester-long), 40 marks
> **Team size:** 3
> **Methodology:** Agile — Scrum, 2-week sprints, incremental requirements engineering
> **Milestone:** M1 (Requirements) — baseline for all downstream phases
> **Date:** 19 August 2026
> **Status:** Baselined. Changes from here on go through Requirements Change Management (Lecture 9, §13).

---

## 1. Purpose and Scope

### 1.1 Problem statement

Conducting objective examinations on paper is slow, manual and error-prone: papers must be printed
and physically secured, OMR sheets must be collected and scanned, and evaluation and result
publication take days. The **Online Examination System** delivers multiple-choice examinations over
the web and evaluates them automatically, reducing the time from submission to result from days to
seconds and removing manual scoring error entirely.

### 1.2 Product scope

A web-based portal in which **Faculty** author multiple-choice questions into a reusable question
bank, assemble and schedule examinations from that bank; **Students** enrolled in the relevant
course attempt those examinations within a defined window under a server-enforced timer; and the
system **evaluates every submission automatically** against a stored answer key and publishes
scorecards on Faculty approval. An **Administrator** manages users, courses and system policy, and
holds the audit trail.

### 1.3 Stakeholders

| Stakeholder | Interest in the system |
|---|---|
| Student / Candidate | Fair, reliable attempt experience; no loss of answers; prompt, explainable results |
| Faculty / Examiner | Fast paper setting from a reusable bank; zero manual evaluation; cohort insight |
| Administrator | Correct user and course data; policy enforcement; auditability |
| Department / Institution | Exam integrity, records retention, compliance with data-protection law |
| Development team (3) | Buildable, testable, demonstrable scope within one semester |

### 1.4 Actors (system boundary)

**Student**, **Faculty**, **Administrator**. There is **no separate Proctor actor** — integrity
monitoring is automated (event logging and flagging) and reviewed by Faculty.

### 1.5 Explicitly out of scope

Descriptive / subjective answers · manual grading and rubrics · webcam or AI proctoring · biometric
identity verification · payments · adaptive or randomised-difficulty testing · native mobile
applications · offline attempt mode · plagiarism detection.

---

## 2. Functional Requirements

Priority uses **MoSCoW**: **M** = Must have (core, committed), **S** = Should have, **C** = Could
have (stretch). Every requirement is written to be *concise, unambiguous, verifiable, measurable,
feasible and traceable* (Lecture 7, "Properties of Requirements").

### 2.1 Module A — User Management & Authentication

| ID | Requirement | Actor | Pri |
|---|---|---|---|
| FR-AUTH-01 | The system shall allow a visitor to register a Student account by submitting full name, institutional email, roll number and password. | Student | M |
| FR-AUTH-02 | The system shall activate a newly registered account only after the user confirms a one-time verification link sent to the registered email. | Student | S |
| FR-AUTH-03 | The system shall authenticate a user against email and password and establish a session on success. | All | M |
| FR-AUTH-04 | The system shall lock an account for 15 minutes after 5 consecutive failed login attempts within a 15-minute period. | All | M |
| FR-AUTH-05 | The system shall allow a user to reset a forgotten password through a single-use link, valid for 15 minutes, sent to the registered email. | All | M |
| FR-AUTH-06 | The system shall assign exactly one role — Student, Faculty or Administrator — to every account, and shall restrict every screen and API endpoint to the roles authorised for it. | All | M |
| FR-AUTH-07 | The system shall permit at most one active session per Student account; establishing a new session shall invalidate the previous one. | Student | M |
| FR-AUTH-08 | The system shall allow a user to view and edit their own name, phone number and password, and shall prevent them from editing their own role or roll number. | All | S |
| FR-AUTH-09 | The system shall terminate a session after 30 minutes of inactivity, except while an examination attempt is in progress. | All | S |
| FR-AUTH-10 | The system shall allow an Administrator to create, deactivate and reactivate any user account. | Admin | M |

### 2.2 Module B — Course & Enrollment Management

| ID | Requirement | Actor | Pri |
|---|---|---|---|
| FR-CRS-01 | The system shall allow an Administrator to create, edit and archive a Course identified by course code, title and semester. | Admin | M |
| FR-CRS-02 | The system shall allow an Administrator to assign one or more Faculty accounts to a Course. | Admin | M |
| FR-CRS-03 | The system shall allow Faculty or an Administrator to enroll Student accounts into a Course individually. | Faculty, Admin | M |
| FR-CRS-04 | The system shall permit a Student to view and attempt only those examinations that belong to Courses in which the Student is enrolled. | Student | M |
| FR-CRS-05 | The system shall allow an Administrator to bulk-import Student accounts and their Course enrollments from a CSV file, and shall report the outcome of every row without committing any row if the file fails validation. | Admin | S |

### 2.3 Module C — Question Bank Management

| ID | Requirement | Actor | Pri |
|---|---|---|---|
| FR-QB-01 | The system shall allow Faculty to create a single-correct multiple-choice question consisting of a question stem, between 2 and 6 options, and exactly one option marked correct. | Faculty | M |
| FR-QB-02 | The system shall allow Faculty to create a multiple-correct question (MSQ) in which two or more options are marked correct. | Faculty | S |
| FR-QB-03 | The system shall allow Faculty to create a True/False question as a two-option multiple-choice question. | Faculty | S |
| FR-QB-04 | The system shall require every question to carry a Course, a topic label, a difficulty level of Easy, Medium or Hard, positive marks, and negative marks. | Faculty | M |
| FR-QB-05 | The system shall prevent modification or deletion of a question that belongs to a published or attempted examination, and shall instead create a new version of that question. | Faculty | M |
| FR-QB-06 | The system shall allow Faculty to import questions in bulk from a defined CSV template, validating every row and rejecting the entire file if any row is invalid. | Faculty | S |
| FR-QB-07 | The system shall allow Faculty to search and filter the question bank by Course, topic, difficulty and keyword in the stem. | Faculty | M |
| FR-QB-08 | The system shall restrict Faculty to creating, viewing and editing questions belonging only to Courses to which they are assigned. | Faculty | M |
| FR-QB-09 | The system shall allow Faculty to attach an optional explanation to a question, to be displayed to Students during post-result answer review. | Faculty | C |
| FR-QB-10 | The system shall allow Faculty to preview a question rendered exactly as a Student will see it during an attempt. | Faculty | C |

### 2.4 Module D — Examination Authoring

| ID | Requirement | Actor | Pri |
|---|---|---|---|
| FR-EX-01 | The system shall allow Faculty to create an Examination with a title, an associated Course, a duration in minutes, a declared total marks value and free-text instructions. | Faculty | M |
| FR-EX-02 | The system shall allow Faculty to add questions to an Examination by selecting them from the question bank. | Faculty | M |
| FR-EX-03 | The system shall allow Faculty to auto-generate an examination paper by specifying the number of questions required per topic and per difficulty level, selecting them at random from the eligible pool. | Faculty | S |
| FR-EX-04 | The system shall compute the sum of question marks and shall prevent publication of an Examination whose computed total does not equal its declared total marks. | Faculty | M |
| FR-EX-05 | The system shall allow Faculty to configure, per Examination: negative marking (enabled/disabled and value), question order shuffling, option order shuffling, backward navigation, and the pass mark. | Faculty | M |
| FR-EX-06 | The system shall hold an Examination in Draft state until Faculty publishes it, and shall make only published Examinations visible to Students. | Faculty | M |
| FR-EX-07 | The system shall prevent any change to an Examination's question set once its examination window has opened or once any attempt exists for it. | Faculty | M |
| FR-EX-08 | The system shall allow Faculty to clone an existing Examination into a new Draft. | Faculty | C |

### 2.5 Module E — Scheduling & Access Control

| ID | Requirement | Actor | Pri |
|---|---|---|---|
| FR-SCH-01 | The system shall allow Faculty to schedule a published Examination by setting a window start date-time and a window end date-time. | Faculty | M |
| FR-SCH-02 | The system shall reject a schedule whose window length is shorter than the Examination's configured duration. | Faculty | M |
| FR-SCH-03 | The system shall present to each Student a dashboard listing the Upcoming, Live and Completed Examinations of the Courses in which the Student is enrolled. | Student | M |
| FR-SCH-04 | The system shall permit a Student to begin an attempt only when the current server time lies within the examination window, the Student is enrolled, and the Student has no previously submitted attempt for that Examination. | Student | M |
| FR-SCH-05 | The system shall refuse to start a new attempt after a configurable late-entry cutoff measured from the window start, defaulting to 15 minutes. | Student | S |
| FR-SCH-06 | The system shall allow Faculty to reschedule or cancel an Examination at any time before its window opens. | Faculty | S |
| FR-SCH-07 | The system shall apply a per-Student additional-time allowance, configured by Faculty, to that Student's attempt duration. | Faculty | S |

### 2.6 Module F — Examination Delivery (Attempt)

| ID | Requirement | Actor | Pri |
|---|---|---|---|
| FR-ATT-01 | The system shall create an attempt record stamped with the server start time when a Student begins an Examination, and shall deliver the paper only after that record exists. | Student | M |
| FR-ATT-02 | The system shall display a countdown timer whose remaining time is derived from the server clock and the attempt start time, and shall not rely on the client clock. | Student | M |
| FR-ATT-03 | The system shall display one question at a time together with a navigation palette showing, for every question, one of four states: Not Visited, Not Answered, Answered, or Marked for Review. | Student | M |
| FR-ATT-04 | The system shall allow a Student to select a response, change a selected response and clear a response at any time before submission. | Student | M |
| FR-ATT-05 | The system shall persist every response to the server within 5 seconds of the Student selecting it, without any explicit save action by the Student. | Student | M |
| FR-ATT-06 | The system shall allow a Student to mark a question for review and to remove that mark. | Student | S |
| FR-ATT-07 | The system shall automatically submit an attempt, retaining all responses persisted up to that instant, when the remaining time reaches zero. | Student | M |
| FR-ATT-08 | The system shall allow a Student whose session was interrupted to resume the same attempt, with remaining time computed from the original server start time and with all previously persisted responses restored. | Student | M |
| FR-ATT-09 | The system shall display a summary of answered, unanswered and marked-for-review counts and require explicit confirmation before accepting a manual submission. | Student | S |
| FR-ATT-10 | The system shall generate a per-Student question and option ordering when shuffling is enabled, and shall store that ordering with the attempt so the attempt can be reconstructed exactly. | Student | M |
| FR-ATT-11 | The system shall reject any attempt to open a second concurrent attempt of the same Examination by the same Student. | Student | M |

### 2.7 Module G — Automatic Evaluation & Scoring

| ID | Requirement | Actor | Pri |
|---|---|---|---|
| FR-EVL-01 | The system shall evaluate every submitted attempt automatically, without any human intervention. | System | M |
| FR-EVL-02 | The system shall award the question's full positive marks for a correct response to a single-correct question, and shall deduct the configured negative marks for an incorrect response. | System | M |
| FR-EVL-03 | The system shall award zero marks and shall apply no negative marking to a question left unattempted. | System | M |
| FR-EVL-04 | The system shall award full marks for a multiple-correct question only when the set of selected options is exactly equal to the set of correct options, and shall otherwise apply the configured partial-credit rule. | System | S |
| FR-EVL-05 | The system shall compute, for every evaluated attempt, the total score, the percentage score and a Pass or Fail outcome against the Examination's configured pass mark. | System | M |
| FR-EVL-06 | The system shall complete the evaluation of a submitted attempt of up to 100 questions within 5 seconds of submission. | System | M |
| FR-EVL-07 | The system shall allow Faculty to correct the answer key of a question after an Examination has ended, shall re-evaluate every affected attempt, and shall record the previous and revised score of each affected attempt in the audit log. | Faculty | S |
| FR-EVL-08 | The system shall allow Faculty to drop a question from scoring after an Examination has ended, and shall re-evaluate every affected attempt excluding that question. | Faculty | S |
| FR-EVL-09 | The system shall retain the raw responses of every attempt so that any published score can be recomputed and justified. | System | M |

### 2.8 Module H — Results & Answer Review

| ID | Requirement | Actor | Pri |
|---|---|---|---|
| FR-RES-01 | The system shall withhold every evaluated result from the Student until Faculty publishes the results of that Examination. | System | M |
| FR-RES-02 | The system shall allow Faculty to publish and to unpublish the results of an Examination. | Faculty | M |
| FR-RES-03 | The system shall display to a Student, for a published result, the total score, the percentage, the Pass or Fail outcome and the marks obtained on each question. | Student | M |
| FR-RES-04 | The system shall display to a Student, when Faculty has enabled answer review, each question together with the Student's response, the correct option or options, and the explanation where one exists. | Student | S |
| FR-RES-05 | The system shall display to Faculty, for each Examination, the mean, median, highest and lowest scores, the pass percentage and the proportion of Students answering each question correctly. | Faculty | S |
| FR-RES-06 | The system shall allow Faculty and Administrators to export the results of an Examination as a CSV file. | Faculty, Admin | M |
| FR-RES-07 | The system shall allow a Student to download their own scorecard as a PDF document. | Student | C |
| FR-RES-08 | The system shall allow a Student to raise a challenge against the answer key of a specific question within a configurable window, defaulting to 48 hours, after result publication. | Student | C |
| FR-RES-09 | The system shall allow Faculty to review a challenge and to accept or reject it, where acceptance initiates the re-evaluation defined in FR-EVL-07. | Faculty | C |

### 2.9 Module I — Examination Integrity

| ID | Requirement | Actor | Pri |
|---|---|---|---|
| FR-INT-01 | The system shall record, with a timestamp, every occurrence of the examination window losing focus during an active attempt. | System | M |
| FR-INT-02 | The system shall display a warning to the Student on each focus-loss event and shall automatically submit the attempt once the number of such events exceeds a configurable threshold, defaulting to 3. | System | S |
| FR-INT-03 | The system shall disable text copy, text paste and the browser context menu within the examination screen. | System | S |
| FR-INT-04 | The system shall flag an attempt whose recorded violation count exceeds the configured threshold and shall present the flag and its supporting event log to Faculty. | System | S |
| FR-INT-05 | The system shall record the IP address and user-agent string associated with every attempt. | System | S |
| FR-INT-06 | The system shall deliver a distinct question and option ordering to each Student when shuffling is enabled for the Examination. | System | M |
| FR-INT-07 | The system shall exclude all correct-answer data from every response delivered to a Student during an active attempt. | System | M |

### 2.10 Module J — Notifications

| ID | Requirement | Actor | Pri |
|---|---|---|---|
| FR-NTF-01 | The system shall send an email to every enrolled Student when an Examination for their Course is scheduled. | System | S |
| FR-NTF-02 | The system shall send an email to every affected Student when the results of an Examination are published. | System | S |
| FR-NTF-03 | The system shall present an in-application notification centre listing the notifications sent to the signed-in user. | System | C |

### 2.11 Module K — Administration & Audit

| ID | Requirement | Actor | Pri |
|---|---|---|---|
| FR-ADM-01 | The system shall write an audit entry recording the actor, action, affected entity, timestamp and changed values for every creation, modification and deletion of a user, question, examination, answer key or result. | System | M |
| FR-ADM-02 | The system shall allow an Administrator to view the audit log and to filter it by actor, entity type and date range. | Admin | S |
| FR-ADM-03 | The system shall allow an Administrator to configure the system-wide default values for session timeout, account lockout policy, late-entry cutoff and violation threshold. | Admin | S |
| FR-ADM-04 | The system shall present to an Administrator a dashboard showing the count of users by role, the count of examinations by state, and the count of attempts in the current day. | Admin | C |

**Functional requirement count:** 74 total — 38 Must, 24 Should, 12 Could.

---

## 3. Non-Functional Requirements

Classified as **Product**, **Organisational** and **External** (Lecture 8, "Non-Functional
Classifications"). Every entry states a **measure** drawn from the metrics table in Lecture 8 §11, so
that each is verifiable rather than aspirational.

### 3.1 Product requirements

| ID | Property | Requirement (measurable) | Verification |
|---|---|---|---|
| NFR-P-01 | Speed | 95% of page loads and API responses shall complete within 2 seconds when 200 attempts are active concurrently. | Load test (JMeter / Locust), 95th-percentile response time |
| NFR-P-02 | Speed | An autosave round trip shall complete within 1 second at 200 concurrent attempts. | Load test, measured round-trip time |
| NFR-P-03 | Speed | Evaluation of a submitted 100-question attempt shall complete within 5 seconds. | Timed integration test |
| NFR-P-04 | Size / Capacity | The system shall sustain at least 200 concurrent attempts and a question bank of at least 50,000 questions without breaching NFR-P-01. | Load test with seeded bank |
| NFR-P-05 | Reliability | The rate of failed attempts caused by system fault shall not exceed 1 in 1,000 attempts. | Defect log across all sprint demos and load runs |
| NFR-P-06 | Availability | The system shall be available for at least 99.5% of the total duration of all published examination windows. | Uptime monitor over the demo period |
| NFR-P-07 | Robustness | After an unplanned server restart, the system shall restore service within 60 seconds, and every in-progress attempt shall remain resumable with all persisted responses intact and the correct remaining time. | Fault-injection test: kill and restart during an active attempt |
| NFR-P-08 | Robustness | The probability of a submitted attempt being left in a partially written state shall be zero; all response and score writes shall be transactional. | Code review of transaction boundaries + concurrent-submission test |
| NFR-P-09 | Ease of use | A first-time Student shall complete a mock attempt unaided after at most 5 minutes of orientation, with a task-success rate of at least 90% across 10 test users. | Usability test session, recorded |
| NFR-P-10 | Ease of use | Every examination-related screen shall be reachable within 3 clicks from the user's dashboard, and context help shall be available on the attempt screen. | Navigation walkthrough |
| NFR-P-11 | Portability | The system shall function correctly on the two most recent versions of Chrome, Edge and Firefox on Windows, macOS and Linux, and shall remain usable at viewport widths of 360 pixels and above. Browser-specific code shall not exceed 5% of front-end statements. | Cross-browser test matrix |
| NFR-P-12 | Maintainability | Automated unit tests shall cover at least 70% of lines in the evaluation and scoring modules, and no function shall exceed a cyclomatic complexity of 10. | Coverage report + static analysis in CI |
| NFR-P-13 | Security (product) | The security requirements SEC-01 to SEC-14 of Section 4 are product non-functional requirements of this system. | See Section 4 |

### 3.2 Organisational requirements

| ID | Requirement | Verification |
|---|---|---|
| NFR-O-01 | Development shall follow Scrum with fixed 2-week sprints, each comprising sprint planning, daily stand-up, sprint review and retrospective, with the artefacts of each ceremony committed to the repository. | Sprint artefact folder per sprint |
| NFR-O-02 | All source code and documentation shall be held in a single Git repository; work shall proceed on feature branches; no commit shall be made directly to `main`; every merge shall be through a pull request reviewed by at least one other team member. | Git history and PR record |
| NFR-O-03 | The team shall maintain an SRS following the IEEE Std 830-1998 table of contents, a Requirements Traceability Matrix updated at every lifecycle phase, and UML use-case, class and sequence diagrams produced before the corresponding implementation begins. | Document review at each milestone |
| NFR-O-04 | All code shall conform to one agreed style guide enforced by a linter executed in continuous integration; a lint failure shall fail the build. | CI configuration and build log |
| NFR-O-05 | Every functional requirement of priority Must shall be linked in the RTM to at least one functional test case identifier. | RTM completeness check |
| NFR-O-06 | Each sprint shall end with a demonstrable, executable increment, tagged in Git. | Git tags and demo recording |
| NFR-O-07 | Each of the three team members shall hold a documented area of ownership, and all work items shall be tracked on a shared board visible to the evaluator. | Board export at each milestone |

### 3.3 External requirements

| ID | Requirement | Verification |
|---|---|---|
| NFR-E-01 | Personal data shall be processed in accordance with the Digital Personal Data Protection Act, 2023: consent shall be obtained at registration, data shall be collected only for the stated examination purpose, and a Student's personal data shall be erasable on request within 30 days. | Privacy notice, consent record, deletion routine |
| NFR-E-02 | Attempt responses and published results shall be retained for at least 3 years to satisfy institutional examination-records policy, and shall be purged thereafter. | Retention configuration and purge job |
| NFR-E-03 | The system shall satisfy WCAG 2.1 Level AA: the entire attempt flow shall be operable by keyboard alone, text contrast shall be at least 4.5:1, and every option control shall carry a programmatic label for screen readers. | Automated accessibility audit + keyboard-only walkthrough |
| NFR-E-04 | Examination results shall be exportable as CSV in a schema accepted by the institution's learning-management system, and the question bank shall be importable and exportable as CSV. | Round-trip import/export test |
| NFR-E-05 | Integrity violation flags shall be presented as advisory evidence for a human decision; the system shall not itself declare a Student guilty of malpractice or void a result automatically. | Design review of the flagging workflow |
| NFR-E-06 | Examination policy values — window, pass mark, negative marking, late entry, violation threshold — shall be configurable at run time and shall not be hard-coded, so that differing departmental policies can be accommodated. | Configuration review |
| NFR-E-07 | The system shall deploy and meet NFR-P-01 on a single commodity Linux virtual machine of 2 vCPU and 4 GB RAM, as available for the academic demonstration. | Deployment on the target VM |

---

## 4. Security Requirements

Derived by the Security Risk Assessment method of Lecture 8: identify assets and stakeholders,
identify threats and attackers, categorise risk, convert each high-priority risk into a SMART
objective, and state the resulting requirement.

### 4.1 Assets and stakeholders

| Asset | Stakeholder | Value |
|---|---|---|
| Question bank with answer keys | Faculty, Institution | Integrity of every future examination; a leak destroys the assessment |
| Live examination paper | Faculty, Students | Fairness; pre-disclosure invalidates the exam |
| Student responses and scores | Student, Institution | Academic record; tangible consequence for the Student |
| User credentials | All users | Account takeover enables impersonation and score tampering |
| Student personal data (name, roll no., email) | Student, Institution | Privacy; legal exposure under DPDP Act 2023 |
| Audit log | Institution | Evidence in any malpractice or grievance proceeding |

### 4.2 Risk assessment

| # | Threat | Attacker | Cost to exploit | Likelihood | Damage | Risk |
|---|---|---|---|---|---|---|
| T1 | Correct answers read from the client payload or browser developer tools during an attempt | Student (external) | Low | High | High | **High** |
| T2 | Score altered by calling the scoring API directly or tampering with a submitted payload | Student (external) | Low | High | High | **High** |
| T3 | Access to another Student's attempt or result by changing an identifier in the request (IDOR) | Student (external) | Low | High | High | **High** |
| T4 | Question paper or answer key retrieved before the examination window opens | Student (external) | Low | Medium | High | **High** |
| T5 | SQL injection or stored XSS through a question stem or profile field | External attacker | Low | Medium | High | **High** |
| T6 | Credential theft by brute force or password reuse, leading to impersonation | External attacker | Medium | Medium | High | **Medium** |
| T7 | Session hijacking allowing a third party to sit the examination | External attacker | Medium | Medium | High | **Medium** |
| T8 | Breach of the personal-data store | External attacker | High | Low | High | **Medium** |
| T9 | Denial of service during an examination window | External attacker | Medium | Low | High | **Medium** |
| T10 | Insider modification of a published score without trace | Faculty (insider) | Low | Low | High | **Medium** |

### 4.3 Security requirements

| ID | Requirement | Mitigates | Pri |
|---|---|---|---|
| SEC-01 | The system shall store user passwords only as salted hashes produced by bcrypt with a cost factor of at least 12, or by Argon2id; storage of plaintext or reversibly encrypted passwords is prohibited. | T6 | M |
| SEC-02 | The system shall serve all traffic over TLS version 1.2 or higher and shall redirect all plain HTTP requests to HTTPS. | T6, T7, T8 | M |
| SEC-03 | The system shall exclude correct-option identifiers, answer keys and explanations from every payload served to a Student role while an attempt is active. | T1 | M |
| SEC-04 | The system shall perform authorisation on the server for every request, verifying both the caller's role and the caller's ownership of the requested resource; no authorisation decision shall depend on a value supplied by the client. | T2, T3, T4 | M |
| SEC-05 | The system shall limit authentication attempts to 5 per account per 15 minutes and shall lock the account for 15 minutes on exceeding that limit. | T6 | M |
| SEC-06 | The system shall access the database exclusively through parameterised queries or an ORM; construction of SQL by string concatenation with user input is prohibited. | T5 | M |
| SEC-07 | The system shall encode all user-supplied content on output and shall enforce a Content-Security-Policy header restricting script sources to the application origin. | T5 | M |
| SEC-08 | The system shall issue session tokens of at least 128 bits of entropy, marked HttpOnly, Secure and SameSite=Strict, and shall issue a new token on every successful authentication. | T7 | M |
| SEC-09 | The system shall make an examination's questions inaccessible to any Student account before the window opens, and its answer keys inaccessible to any Student account until results are published. | T4 | M |
| SEC-10 | The system shall compute every score on the server from stored responses; a score, percentage or outcome supplied by a client shall be rejected. | T2 | M |
| SEC-11 | The audit log shall be append-only; no role, including Administrator, shall be able to modify or delete an existing audit entry. | T10 | M |
| SEC-12 | The system shall encrypt personal data and stored attempt responses at rest using AES-256, and shall encrypt every database backup. | T8 | S |
| SEC-13 | The system shall rate-limit each authenticated session to at most 100 requests per minute across all endpoints. | T9 | S |
| SEC-14 | The team shall scan all third-party dependencies for known vulnerabilities once per sprint, and shall not release an increment containing a dependency with a known High or Critical severity vulnerability. | T5, T8 | S |

### 4.4 SMART security objectives

| ID | Specific | Measurable | Time-bound |
|---|---|---|---|
| SO-1 | No answer-key field reachable by a Student role during an attempt | 0 occurrences across an automated API response-inspection suite | Before Sprint 2 review |
| SO-2 | All scoring performed server-side | 100% of score-writing paths originate in the evaluation service, verified by code review | Before Sprint 3 review |
| SO-3 | Credentials protected | 100% of stored passwords are Argon2id or bcrypt hashes; brute-force lockout demonstrated | Before Sprint 1 review |
| SO-4 | Transport protected | TLS 1.2+ on all endpoints; 0 endpoints reachable over plain HTTP | Before first deployment |
| SO-5 | Injection resistant | 0 High or Critical findings from an OWASP ZAP baseline scan | Before Sprint 4 review |

---

## 5. User Stories (Product Backlog)

Format: *As a `<role>`, I want `<goal>` so that `<benefit>`.* Estimated in story points on a modified
Fibonacci scale. The **FRs** column gives traceability back to Section 2 and becomes the first
linkage column of the RTM.

### Epic 1 — Access & Identity

| ID | User story | FRs | Pts | Sprint |
|---|---|---|---|---|
| US-01 | As a **Student**, I want to register with my institutional email and roll number so that I can be identified as a genuine candidate of my college. | FR-AUTH-01, FR-AUTH-02 | 3 | 1 |
| US-02 | As **any user**, I want to sign in and be taken to a dashboard appropriate to my role so that I only see what concerns me. | FR-AUTH-03, FR-AUTH-06 | 5 | 1 |
| US-03 | As a **Student**, I want my account locked after repeated failed sign-ins so that nobody can guess my password and sit my exam. | FR-AUTH-04, SEC-05 | 2 | 1 |
| US-04 | As **any user**, I want to reset a forgotten password through my email so that I am never locked out on the morning of an exam. | FR-AUTH-05 | 3 | 1 |
| US-05 | As an **Administrator**, I want to create, deactivate and reactivate accounts so that only current members of the institution can use the portal. | FR-AUTH-10 | 3 | 1 |

### Epic 2 — Course & Cohort Setup

| ID | User story | FRs | Pts | Sprint |
|---|---|---|---|---|
| US-06 | As an **Administrator**, I want to create courses and assign faculty to them so that every exam has a clear owner. | FR-CRS-01, FR-CRS-02 | 3 | 1 |
| US-07 | As **Faculty**, I want to enroll my students into my course so that only my class can see and attempt my exams. | FR-CRS-03, FR-CRS-04 | 5 | 1 |
| US-08 | As an **Administrator**, I want to upload a CSV of students and enrollments so that I do not have to add a hundred accounts by hand. | FR-CRS-05 | 5 | 2 |

### Epic 3 — Question Bank

| ID | User story | FRs | Pts | Sprint |
|---|---|---|---|---|
| US-09 | As **Faculty**, I want to write a multiple-choice question with options and mark the correct one so that I can build a reusable bank instead of retyping papers each semester. | FR-QB-01, FR-QB-04 | 5 | 2 |
| US-10 | As **Faculty**, I want to tag every question with topic and difficulty so that I can later assemble a balanced paper automatically. | FR-QB-04, FR-QB-07 | 3 | 2 |
| US-11 | As **Faculty**, I want to set multiple-correct and True/False questions so that the bank matches the variety of my actual question papers. | FR-QB-02, FR-QB-03 | 5 | 3 |
| US-12 | As **Faculty**, I want the system to stop me editing a question that a student has already answered so that a live exam can never change under a candidate. | FR-QB-05 | 3 | 2 |
| US-13 | As **Faculty**, I want to import questions from a CSV file so that I can move an existing question paper into the bank in one step. | FR-QB-06 | 5 | 3 |

### Epic 4 — Exam Authoring & Scheduling

| ID | User story | FRs | Pts | Sprint |
|---|---|---|---|---|
| US-14 | As **Faculty**, I want to assemble an exam by picking questions from the bank and setting duration and total marks so that I can set a paper in minutes. | FR-EX-01, FR-EX-02, FR-EX-04 | 8 | 2 |
| US-15 | As **Faculty**, I want to configure negative marking, shuffling and the pass mark per exam so that the portal matches my department's assessment policy rather than forcing one of its own. | FR-EX-05, NFR-E-06 | 3 | 2 |
| US-16 | As **Faculty**, I want to auto-generate a paper by specifying how many easy, medium and hard questions I need per topic so that every student sits a balanced paper without me hand-picking sixty questions. | FR-EX-03 | 8 | 3 |
| US-17 | As **Faculty**, I want to schedule an exam for a fixed window and publish it so that students know exactly when they may attempt it. | FR-SCH-01, FR-SCH-02, FR-EX-06 | 5 | 2 |
| US-18 | As a **Student**, I want a dashboard of my upcoming, live and completed exams so that I never miss a paper. | FR-SCH-03 | 3 | 2 |

### Epic 5 — Taking the Exam

| ID | User story | FRs | Pts | Sprint |
|---|---|---|---|---|
| US-19 | As a **Student**, I want to start my exam only within its window and see a timer counting down so that the conditions are identical for everyone. | FR-SCH-04, FR-ATT-01, FR-ATT-02 | 8 | 3 |
| US-20 | As a **Student**, I want a question palette showing what I have answered, skipped or marked for review so that I can manage my time across the paper. | FR-ATT-03, FR-ATT-06 | 5 | 3 |
| US-21 | As a **Student**, I want every answer saved the moment I select it so that a browser crash or a dropped connection never costs me my work. | FR-ATT-04, FR-ATT-05 | 8 | 3 |
| US-22 | As a **Student**, I want to resume my attempt after a disconnection with my remaining time intact so that a network problem does not become an academic penalty. | FR-ATT-08, NFR-P-07 | 8 | 3 |
| US-23 | As a **Student**, I want the paper submitted automatically when time runs out so that I am not penalised for a late click. | FR-ATT-07 | 3 | 3 |
| US-24 | As **Faculty**, I want each student to receive a different question and option order so that copying from a neighbouring screen gains nothing. | FR-ATT-10, FR-INT-06 | 5 | 3 |

### Epic 6 — Automatic Evaluation

| ID | User story | FRs | Pts | Sprint |
|---|---|---|---|---|
| US-25 | As **Faculty**, I want every submitted paper scored automatically against the answer key so that I never evaluate an objective paper by hand again. | FR-EVL-01, FR-EVL-02, FR-EVL-05 | 8 | 4 |
| US-26 | As a **Student**, I want unattempted questions to carry no negative marks so that the scoring matches the rules stated on my instruction sheet. | FR-EVL-03 | 2 | 4 |
| US-27 | As **Faculty**, I want to correct a wrong answer key after the exam and have every affected paper re-scored automatically so that one bad key does not require re-evaluating the whole class by hand. | FR-EVL-07, FR-EVL-08 | 8 | 4 |
| US-28 | As an **Administrator**, I want every score change recorded with who changed it and what it was before so that any grievance can be settled from the record. | FR-ADM-01, SEC-11 | 5 | 4 |

### Epic 7 — Results & Review

| ID | User story | FRs | Pts | Sprint |
|---|---|---|---|---|
| US-29 | As **Faculty**, I want results held back until I publish them so that I can sanity-check the paper before the class sees its marks. | FR-RES-01, FR-RES-02 | 3 | 4 |
| US-30 | As a **Student**, I want my scorecard with per-question marks so that I understand exactly how my total was arrived at. | FR-RES-03 | 5 | 4 |
| US-31 | As a **Student**, I want to review each question with my answer, the correct answer and an explanation so that the exam teaches me something after it ends. | FR-RES-04, FR-QB-09 | 5 | 4 |
| US-32 | As **Faculty**, I want class statistics and per-question correct-answer rates so that I can tell which questions were bad rather than which students were weak. | FR-RES-05 | 5 | 4 |
| US-33 | As **Faculty**, I want to export results as CSV so that I can upload marks into the institution's records without retyping. | FR-RES-06, NFR-E-04 | 3 | 4 |

### Epic 8 — Integrity & Audit

| ID | User story | FRs | Pts | Sprint |
|---|---|---|---|---|
| US-34 | As **Faculty**, I want tab-switching during an attempt logged and the student warned so that candidates are deterred from consulting another window. | FR-INT-01, FR-INT-02 | 5 | 3 |
| US-35 | As **Faculty**, I want attempts with excessive violations flagged for my review so that I decide on malpractice, not the software. | FR-INT-04, NFR-E-05 | 3 | 4 |
| US-36 | As a **Student**, I want to be certain the correct answers are never sent to my browser during the exam so that the paper is fair to those who do not inspect network traffic. | FR-INT-07, SEC-03 | 5 | 3 |

**Backlog totals:** 8 epics, 36 stories, 178 story points.

---

## 6. Constraints, Assumptions and Dependencies

### 6.1 Design constraints

The implementation stack is **deliberately not fixed at M1**, in keeping with the principle that a
requirement states *what*, not *how* (Lecture 7 §6). The stack decision is a Sprint 0 activity and
will be recorded as an addendum to this document under Requirements Change Management. Constraints
already binding: a web application reachable over HTTPS from a standard browser; a relational
database, since scoring, enrollment and audit are all inherently relational; deployable on the
2 vCPU / 4 GB virtual machine of NFR-E-07.

### 6.2 Assumptions

Students have a personal device with a supported browser and a broadband or mobile connection ·
examinations are attempted remotely, not in a supervised laboratory · the institution supplies
authoritative course and enrollment data · an SMTP relay is available for email notification ·
server time is synchronised via NTP, since every timing rule depends on it.

### 6.3 Dependencies

Email delivery service (FR-NTF-01, FR-NTF-02) · TLS certificate for the deployment host (SEC-02) ·
CSV schema agreed with the institution's LMS (NFR-E-04) · hosting virtual machine availability for
the end-of-semester demonstration.

### 6.4 Known risks to the requirements themselves

Concurrency under load (NFR-P-01, NFR-P-04) is the requirement most likely to fail late, and is
therefore load-tested from Sprint 3 rather than at the end · the auto-generation algorithm
(FR-EX-03) may prove harder than estimated and is a Should, droppable without affecting the core
demonstration · the answer-key challenge flow (FR-RES-08, FR-RES-09) is the designated scope-release
valve if Sprint 4 runs tight.

---

## 7. Team Roles

| Member | Role | Owns |
|---|---|---|
| **Kshitij** (repo owner) | Backend & data lead | Schema, authentication and RBAC, attempt lifecycle, evaluation engine, audit log, unit tests |
| **Kartik** | Frontend & UX lead | Student attempt interface, palette and timer, faculty authoring screens, accessibility compliance (NFR-E-03), usability testing |
| **Komal** | QA, docs & delivery lead | SRS and RTM upkeep, UML diagrams, test plan and test cases, CI pipeline and linting, load and security testing, sprint artefacts, demo script |

All three: peer review of every pull request (NFR-O-02); shared responsibility for sprint ceremonies
and the final viva.

---

## 8. Traceability Seed (RTM skeleton)

The Requirements Traceability Matrix is opened at M1 with its first two columns populated, and is
progressively filled by each later phase (Lecture 9 §12). Forward tracing runs requirement → design →
code → test; backward tracing runs test → requirement.

| Req ID | User Story | Architectural Section | Design Section | File / Implementation | Unit Test ID | Functional Test ID | System Test ID | Acceptance Test ID |
|---|---|---|---|---|---|---|---|---|
| FR-AUTH-03 | US-02 | *M2* | *M3* | *M3* | *M3* | *M4* | *M4* | *M4* |
| FR-EVL-02 | US-25 | *M2* | *M3* | *M3* | *M3* | *M4* | *M4* | *M4* |
| … | … | … | … | … | … | … | … | … |

*(To be populated for all 74 functional requirements in the RTM workbook; the table above shows the
shape only.)*

---

## 9. Milestone Plan

| Milestone | Deliverable | Sprint |
|---|---|---|
| **M1** | Requirements commitment — this document: FRs, NFRs, security requirements, user stories, backlog | Sprint 0 |
| **M2** | SRS (IEEE Std 830-1998), UML use-case and class diagrams, architecture, stack decision | Sprint 1 |
| **M3** | Design documents, ERD, sequence diagrams, working increment of Epics 1–4 | Sprints 2–3 |
| **M4** | Working increment of Epics 5–8, test plan, executed test cases, completed RTM | Sprint 4 |
| **M5** | Final demonstration, deployment, retrospective report | End of semester |

---

## 10. Requirements Validation

Per Lecture 9 §8–10, this baseline is validated by a **requirements review** conducted by all three
members against the properties checklist of Lecture 7; a **prototype** of the attempt screen, since
the system is heavily interactive and prototyping is most beneficial in exactly such systems; and
**acceptance criteria** written for every Must-priority requirement before Sprint 2 opens.

**Change control:** any change to a baselined requirement is raised as a change request, assessed for
impact on scope, schedule and the RTM, and recorded in `docs/CHANGELOG.md` against its sprint.
