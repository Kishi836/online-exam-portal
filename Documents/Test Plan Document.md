# Test Plan Document — Online Examination Portal

**Course:** UE23CS341A — Software Engineering, PES University, Dept. of CSE
**Project:** Online Examination System with Multiple-Choice Questions and Evaluation
**Author / Tester:** Kshitij G Shettigar (Backend & Data Lead)
**Version:** 2.0 · **Date:** 2026-09-02
**Status:** Test design complete; execution pending implementation

---

## 1. Purpose

Test cases for the Online Examination Portal, written to the template issued in
`Test Plan Document.docx`. Coverage is **8–10 test cases per use case** across **13 use cases**,
spanning **Unit, Integration and System** testing, and collectively exercising **all 30 functional
requirements** of the reduced baseline in `Documents/SRS Document.md`.

## 2. Test Case ID convention

Per the template's guidance (*"follow some convention like `UT_01`"*):

| Prefix | Test type | What it exercises |
|---|---|---|
| `UT_nnn` | **Unit test** | One function, validator or rule in isolation — field validation, a scoring calculation, a state transition |
| `IT_nnn` | **Integration test** | Two or more components together — API to database, service to mailer, UI to API |
| `ST_nnn` | **System test** | An end-to-end flow through the running system as a real actor would drive it |

Numbering is a single running sequence per prefix, so an ID is never reused if a case is later
inserted or retired.

## 3. Traceability

Every test case description opens with the requirement ID it verifies, so this document feeds the
test-case columns of the Requirements Traceability Matrix without a separate mapping table.
Identifiers are the `FR-*` space shared by the PRD, the SRS and the RTM.

## 4. Testing environment

| | |
|---|---|
| Environment name | `TEST` — dedicated test instance, seeded database, isolated from demo data |
| Client | Google Chrome (latest stable) on Windows 11, 1920×1080; a second browser profile where a test needs two concurrent sessions |
| Server | Application server with an NTP-synchronised system clock |
| Mail | Captured SMTP sink, so system mail is readable without a live mailbox |
| Data | Seeded fixture set — see §5 |

## 5. Standing test fixtures

Referenced by name in the *Test data* column so precise values are not repeated in every row.

| Fixture | Value |
|---|---|
| `STU_A` | `stu.a@pesu.pes.edu` / `Passw0rd!A` / roll `PES1UG24CS001`, role Student, active |
| `STU_B` | `stu.b@pesu.pes.edu` / `Passw0rd!B` / roll `PES1UG24CS002`, role Student, active |
| `FAC_A` | `fac.a@pes.edu` / `Fac#2026A`, role Faculty, assigned to `CRS_X` |
| `FAC_B` | `fac.b@pes.edu` / `Fac#2026B`, role Faculty, assigned to `CRS_Y` only |
| `ADM_A` | `admin@pes.edu` / `Adm#2026A`, role Administrator |
| `CRS_X` | Course `UE24CS351A` / "Database Management Systems" / Semester 5, active |
| `CRS_Y` | Course `UE24CS342AA5` / "Advanced Virtual Reality" / Semester 5, active |
| `EXM_1` | Examination "DBMS Unit Test 1", `CRS_X`, 60 min, declared total 50, 25 questions, published |
| `Q_SC1` | Single-correct MCQ, 4 options, correct = option B, +2 marks, −0.5 negative |

## 6. How the result columns are used

*Actual Result* and *Test Result* are deliberately **left blank**. The template requires them to be
populated from manual execution, and no implementation exists yet — the project is at the
requirements stage and code begins at M3. Filling them now would be fabrication. They are populated
during the M4 execution pass, once the increment for the relevant module is running.

---

## UC-01 — Register a Student account

Verifies `FR-AUTH-01`.

| Test Case ID | Name of Module | Test case description | Pre-conditions | Test Steps | Test data | Expected Results | Actual Result | Test Result |
|---|---|---|---|---|---|---|---|---|
| UT_001 | User Registration | FR-AUTH-01 — Register with all four mandatory fields valid | Registration page reachable; no account exists for the email or roll number | 1: Open `/register` 2: Enter full name, institutional email, roll number, password 3: Click Register | Name `Arjun Rao`, email `arjun.rao@pesu.pes.edu`, roll `PES1UG24CS111`, password `Str0ng#Pass` | Account created with role Student; message "Registration successful" | | |
| UT_002 | User Registration | FR-AUTH-01 — Reject submission with a mandatory field left empty | Registration page reachable | 1: Open `/register` 2: Leave Roll Number empty 3: Complete the other three fields 4: Click Register | Name `Arjun Rao`, email `arjun.rao@pesu.pes.edu`, roll `` (empty), password `Str0ng#Pass` | Registration rejected; no account created; inline error "Roll number is required" | | |
| UT_003 | User Registration | FR-AUTH-01 — Reject a non-institutional email domain | Registration page reachable; accepted domain configured as `pesu.pes.edu` | 1: Open `/register` 2: Enter a personal email 3: Complete remaining fields 4: Click Register | Email `arjun.rao@gmail.com`, other fields valid | Registration rejected; error "Please register with your institutional email address" | | |
| UT_004 | User Registration | FR-AUTH-01 — Reject a malformed email address | Registration page reachable | 1: Open `/register` 2: Enter an email with no `@` 3: Complete remaining fields 4: Click Register | Email `arjun.rao.pesu.pes.edu`, other fields valid | Registration rejected; error "Enter a valid email address"; no account created | | |
| UT_005 | User Registration | FR-AUTH-01 — Reject a duplicate institutional email | `STU_A` already registered | 1: Open `/register` 2: Enter `STU_A`'s email with a fresh roll number 3: Click Register | Email `stu.a@pesu.pes.edu`, roll `PES1UG24CS999` | Registration rejected; error "An account with this email already exists"; `STU_A` unmodified | | |
| UT_006 | User Registration | FR-AUTH-01 — Reject a duplicate roll number | `STU_A` already registered | 1: Open `/register` 2: Enter a fresh email with `STU_A`'s roll number 3: Click Register | Email `new.student@pesu.pes.edu`, roll `PES1UG24CS001` | Registration rejected; error "This roll number is already registered" | | |
| IT_001 | User Registration | FR-AUTH-01 — Registration persists a Student row with a hashed password | Test database reachable and inspectable | 1: Register a new Student 2: Query the users table for that email 3: Inspect the stored password column | Email `arjun.rao@pesu.pes.edu`, password `Str0ng#Pass` | Exactly one row exists; role is `STUDENT`; the password column holds a salted hash; the literal `Str0ng#Pass` appears nowhere in the database or logs | | |
| IT_002 | User Registration | FR-AUTH-01 — Two concurrent registrations of the same roll number produce one account | Test database reachable; no account for roll `PES1UG24CS222` | 1: Fire two registration requests with the same roll number simultaneously 2: Query the users table | Two requests, both roll `PES1UG24CS222`, different emails | Exactly one account is created; the other is rejected as a duplicate; no partial or orphaned row | | |
| ST_001 | User Registration | FR-AUTH-01 — End-to-end registration through to a usable account | `TEST` environment running | 1: Open the portal as an anonymous visitor 2: Register with valid details 3: Sign in with the new credentials 4: Confirm the Student dashboard loads | Name `Arjun Rao`, email `arjun.rao@pesu.pes.edu`, roll `PES1UG24CS111`, password `Str0ng#Pass` | Registration succeeds and the new account can immediately sign in and reach the Student dashboard | | |

## UC-02 — Sign in and reach a role-appropriate dashboard

Verifies `FR-AUTH-03`, `FR-AUTH-06`.

| Test Case ID | Name of Module | Test case description | Pre-conditions | Test Steps | Test data | Expected Results | Actual Result | Test Result |
|---|---|---|---|---|---|---|---|---|
| UT_007 | Authentication | FR-AUTH-03 — Sign in with correct credentials | `STU_A` exists and is active | 1: Open `/login` 2: Enter email and password 3: Click Sign in | `stu.a@pesu.pes.edu` / `Passw0rd!A` | Sign-in succeeds; a session is established; the Student dashboard is displayed | | |
| UT_008 | Authentication | FR-AUTH-03 — Reject a correct email with a wrong password | `STU_A` exists and is active | 1: Open `/login` 2: Enter the correct email and a wrong password 3: Click Sign in | `stu.a@pesu.pes.edu` / `WrongPass1` | Sign-in refused; no session established; message "Invalid email or password" — it does not reveal that the email exists | | |
| UT_009 | Authentication | FR-AUTH-03 — Reject an unknown email without disclosing that it is unknown | No account exists for the email used | 1: Open `/login` 2: Enter an unregistered email and any password 3: Click Sign in | `nobody@pesu.pes.edu` / `AnyPass123` | Sign-in refused with the identical message and a comparable response time to UT_008, so accounts cannot be enumerated | | |
| UT_010 | Authentication | FR-AUTH-03 — Reject sign-in with an empty password | `STU_A` exists | 1: Open `/login` 2: Enter a valid email and leave the password empty 3: Click Sign in | `stu.a@pesu.pes.edu` / `` (empty) | Sign-in refused; inline error "Password is required"; no authentication attempt is recorded | | |
| UT_011 | Authorization | FR-AUTH-06 — Every account carries exactly one role | `STU_A`, `FAC_A` and `ADM_A` exist | 1: Query the stored record for each of the three accounts 2: Inspect the role field | The three fixture accounts | Each holds exactly one role, drawn from Student, Faculty or Administrator; no account holds none or more than one | | |
| IT_003 | Authentication | FR-AUTH-03 — The session identifier is regenerated on sign-in | `STU_A` exists; browser developer tools available | 1: Load `/login` and record the pre-authentication session cookie 2: Sign in successfully 3: Record the cookie again and compare | `stu.a@pesu.pes.edu` / `Passw0rd!A` | The identifier differs before and after; the pre-authentication identifier is invalidated, so a fixated session cannot be reused | | |
| IT_004 | Authorization | FR-AUTH-06 — A Student is refused a Faculty-only API endpoint called directly | `STU_A` signed in | 1: Sign in as `STU_A` 2: Using the session token, call `POST /api/questions` directly, bypassing the UI 3: Inspect the response | Valid Student session token; a well-formed question payload | Response is HTTP 403; no question is created; the body carries no Faculty data | | |
| IT_005 | Authorization | FR-AUTH-06 — A Faculty member is refused an Administrator-only endpoint | `FAC_A` signed in | 1: Sign in as `FAC_A` 2: Call `POST /api/admin/courses` with a valid payload 3: Inspect the response | Valid Faculty session token; a well-formed course payload | Response is HTTP 403; no course is created | | |
| IT_006 | Authorization | FR-AUTH-06 — An unauthenticated client is refused every protected endpoint | Application running; no session held | 1: Enumerate the application's endpoints 2: Call each with no session cookie, excluding sign-in and registration 3: Record each status code | The full endpoint list | Every protected endpoint returns HTTP 401; no endpoint defaults to open | | |
| ST_002 | Authentication & Authorization | FR-AUTH-03, FR-AUTH-06 — Each role lands on its own dashboard and cannot reach another's | `STU_A`, `FAC_A`, `ADM_A` exist and are active | 1: Sign in as `STU_A`, note the landing page, attempt `/faculty/questions`, sign out 2: Repeat as `FAC_A`, attempting `/admin/courses` 3: Repeat as `ADM_A`, confirming the admin dashboard loads | The three fixture accounts | Each role lands on its own dashboard; every cross-role navigation is refused with HTTP 403 and an authorisation message; no other role's data is rendered | | |

## UC-03 — Manage courses and assign faculty

Verifies `FR-CRS-01`.

| Test Case ID | Name of Module | Test case description | Pre-conditions | Test Steps | Test data | Expected Results | Actual Result | Test Result |
|---|---|---|---|---|---|---|---|---|
| UT_012 | Course Management | FR-CRS-01 — Create a course with code, title and semester | `ADM_A` signed in | 1: Open `/admin/courses` 2: Click New course 3: Enter code, title and semester 4: Save | Code `UE24CS351A`, title `Database Management Systems`, semester `5` | The course is created and listed as Active; message "Course created" | | |
| UT_013 | Course Management | FR-CRS-01 — Reject a course with any mandatory field empty | `ADM_A` signed in | 1: Open the New course form 2: Leave the Title empty 3: Complete code and semester 4: Save | Code `UE24CS999A`, title `` (empty), semester `5` | Creation rejected; inline error "Course title is required"; no course created | | |
| UT_014 | Course Management | FR-CRS-01 — Reject a duplicate code within the same semester | `CRS_X` exists as `UE24CS351A` in semester 5 | 1: Open the New course form 2: Enter the same code and semester with a different title 3: Save | Code `UE24CS351A`, title `DBMS Repeat`, semester `5` | Creation rejected; error "A course with this code already exists for the selected semester" | | |
| UT_015 | Course Management | FR-CRS-01 — Reject assigning a non-Faculty account as Faculty | `CRS_X` exists; `STU_A` is a Student | 1: Open `CRS_X` 2: Open the Assign faculty picker 3: Attempt to assign `STU_A` | `STU_A` = `stu.a@pesu.pes.edu` | The assignment is rejected; only Faculty-role accounts are selectable, or the attempt raises "Only Faculty accounts can be assigned to a course" | | |
| UT_016 | Course Management | FR-CRS-01 — Reject a duplicate faculty assignment | `FAC_A` already assigned to `CRS_X` | 1: Open `CRS_X` 2: Assign `FAC_A` again 3: Inspect the assigned list | `FAC_A` on `CRS_X` | The duplicate is rejected or ignored; `FAC_A` appears exactly once | | |
| IT_007 | Course Management | FR-CRS-01 — Archiving preserves history while blocking new work | `CRS_X` has enrolled Students and one completed examination | 1: As `ADM_A`, archive `CRS_X` 2: Attempt to create a new examination under it 3: Open its past examination's results | `CRS_X` with `EXM_1` completed | New examinations and enrollments are refused with "This course is archived"; the existing examination, attempts and results remain readable | | |
| IT_008 | Course Management | FR-CRS-01 — Assigning a second faculty grants both authoring rights | `CRS_X` assigned to `FAC_A` only | 1: As `ADM_A`, assign `FAC_B` to `CRS_X` 2: Sign in as `FAC_B` 3: Create a question under `CRS_X` | `FAC_B` newly assigned to `CRS_X` | `CRS_X` appears in `FAC_B`'s course list and the question is created successfully | | |
| ST_003 | Course Management | FR-CRS-01 — End-to-end course setup by an Administrator | `TEST` environment running | 1: Sign in as `ADM_A` 2: Create a course 3: Assign `FAC_A` to it 4: Sign in as `FAC_A` and confirm the course is listed 5: Archive the course as `ADM_A` 6: Confirm `FAC_A` can no longer add examinations to it | Code `UE24CS360A`, title `Operating Systems`, semester `5`; `FAC_A` | Every stage behaves as specified; the archived course remains readable but closed to new work | | |

## UC-04 — Enroll students and gate examination visibility

Verifies `FR-CRS-03`, `FR-CRS-04`.

| Test Case ID | Name of Module | Test case description | Pre-conditions | Test Steps | Test data | Expected Results | Actual Result | Test Result |
|---|---|---|---|---|---|---|---|---|
| UT_017 | Enrollment | FR-CRS-03 — Faculty enrolls a Student into their own course | `FAC_A` signed in and assigned to `CRS_X`; `STU_A` exists | 1: Open `CRS_X` 2: Click Enroll student 3: Search for `STU_A` and confirm | `STU_A` = roll `PES1UG24CS001` | `STU_A` appears on the `CRS_X` roster; message "Student enrolled" | | |
| UT_018 | Enrollment | FR-CRS-03 — Reject a duplicate enrollment | `STU_A` already enrolled in `CRS_X` | 1: Open `CRS_X` 2: Enroll `STU_A` again 3: Inspect the roster | `STU_A` on `CRS_X` | The duplicate is rejected with "This student is already enrolled"; the roster shows `STU_A` once | | |
| UT_019 | Enrollment | FR-CRS-03 — Reject enrolling a Faculty or Administrator account | `FAC_A` signed in on `CRS_X` | 1: Open the Enroll student picker 2: Search for `FAC_B` and attempt to enroll | `FAC_B` = `fac.b@pes.edu` | The enrollment is rejected; only Student-role accounts are selectable, or the attempt raises "Only Student accounts can be enrolled" | | |
| UT_020 | Enrollment | FR-CRS-03 — Faculty cannot enroll into a course they are not assigned to | `FAC_B` assigned to `CRS_Y` only | 1: Sign in as `FAC_B` 2: Call the enroll endpoint for `CRS_X` directly | `FAC_B`, target `CRS_X`, student `STU_A` | The call is refused with HTTP 403; no enrollment is created | | |
| UT_021 | Enrollment | FR-CRS-04 — A Student sees only the examinations of enrolled courses | `STU_A` enrolled in `CRS_X` only; both `CRS_X` and `CRS_Y` have published examinations | 1: Sign in as `STU_A` 2: Open the dashboard 3: List the examinations shown | `STU_A`; `CRS_X` and `CRS_Y` each with one published exam | Only the `CRS_X` examination is listed; the `CRS_Y` examination does not appear | | |
| IT_009 | Enrollment | FR-CRS-04 — Direct URL access to a non-enrolled examination is refused | `STU_A` not enrolled in `CRS_Y`; a `CRS_Y` examination exists with a known ID | 1: Sign in as `STU_A` 2: Request the `CRS_Y` examination URL directly 3: Inspect the response | `STU_A`; `CRS_Y` examination ID | Response is HTTP 403; no title, instructions or questions appear in the body | | |
| IT_010 | Enrollment | FR-CRS-04 — The start-attempt endpoint refuses a non-enrolled Student | `STU_A` not enrolled in `CRS_Y`; a live `CRS_Y` examination exists | 1: Sign in as `STU_A` 2: Call `POST /api/attempts` for the `CRS_Y` examination 3: Query the attempts table | `STU_A`; live `CRS_Y` examination | The call is refused with HTTP 403; no attempt record is created | | |
| IT_011 | Enrollment | FR-CRS-04 — Unenrolling removes an upcoming examination from the dashboard | `STU_A` enrolled in `CRS_X`, which has an upcoming examination | 1: Confirm the examination is listed 2: As `FAC_A`, remove `STU_A` from `CRS_X` 3: Refresh the dashboard 4: Attempt to start the examination | `STU_A`, `CRS_X`, upcoming `EXM_1` | The examination disappears from the dashboard and cannot be started | | |
| ST_004 | Enrollment | FR-CRS-03, FR-CRS-04 — End-to-end cohort isolation between two courses | `TEST` environment; `CRS_X` and `CRS_Y` each with a published examination | 1: As `FAC_A`, enroll `STU_A` into `CRS_X` 2: As `FAC_B`, enroll `STU_B` into `CRS_Y` 3: Sign in as `STU_A` and list visible examinations 4: Sign in as `STU_B` and do the same 5: From each account, request the other's examination URL | `STU_A` → `CRS_X`; `STU_B` → `CRS_Y` | Each Student sees only their own course's examination; each cross-course URL request is refused with HTTP 403 | | |

## UC-05 — Author and manage question bank entries

Verifies `FR-QB-01`, `FR-QB-04`, `FR-QB-05`.

| Test Case ID | Name of Module | Test case description | Pre-conditions | Test Steps | Test data | Expected Results | Actual Result | Test Result |
|---|---|---|---|---|---|---|---|---|
| UT_022 | Question Bank | FR-QB-01 — Create a single-correct MCQ with four options | `FAC_A` signed in and assigned to `CRS_X` | 1: Open `/faculty/questions/new` 2: Enter the stem 3: Add four options and mark one correct 4: Complete the metadata 5: Save | Stem `Which normal form removes transitive dependency?`, options `1NF/2NF/3NF/BCNF`, correct `3NF` | The question is saved to the `CRS_X` bank and appears in the question list | | |
| UT_023 | Question Bank | FR-QB-01 — Reject a question with fewer than two options | `FAC_A` signed in | 1: Open the new question form 2: Enter a stem and a single option 3: Save | Stem valid, one option `3NF` | Creation rejected; error "A question must have between 2 and 6 options" | | |
| UT_024 | Question Bank | FR-QB-01 — Reject a question with more than six options | `FAC_A` signed in | 1: Open the new question form 2: Enter a stem and seven options 3: Save | Stem valid, seven options `A`–`G` | Creation rejected with the same boundary message; no question is created | | |
| UT_025 | Question Bank | FR-QB-01 — Reject a question with no option marked correct | `FAC_A` signed in | 1: Enter a stem and four options 2: Mark none as correct 3: Save | Four options, zero marked correct | Creation rejected; error "Exactly one option must be marked correct" | | |
| UT_026 | Question Bank | FR-QB-01 — Reject a single-correct question with two options marked correct | `FAC_A` signed in | 1: Enter a stem and four options 2: Mark two as correct 3: Save | Four options, `2NF` and `3NF` both marked correct | Creation rejected with the same message; exactly one correct option is required | | |
| UT_027 | Question Bank | FR-QB-04 — Reject a question missing any mandatory metadata field | `FAC_A` signed in | 1: Enter a valid stem and options 2: Leave Difficulty unset 3: Save; repeat for course, topic, marks and negative marks | Stem and options valid; one metadata field empty each time | Each is rejected with an inline error naming the missing field; no question is created | | |
| IT_012 | Question Bank | FR-QB-04 — Reject a difficulty value outside the permitted set | `FAC_A` signed in; API reachable | 1: Submit a question via the API with an invalid difficulty 2: Inspect the response | Difficulty `Impossible` | Rejected with HTTP 400 and "Difficulty must be one of Easy, Medium or Hard" | | |
| IT_013 | Question Bank | FR-QB-05 — A question in a published examination cannot be edited in place | `Q_SC1` is attached to `EXM_1`, which is published | 1: Sign in as `FAC_A` 2: Open `Q_SC1` 3: Change the stem 4: Save 5: Query the question table | `Q_SC1`, new stem text | The in-place edit is refused; a **new version** is created instead; the version attached to `EXM_1` is byte-identical to before | | |
| IT_014 | Question Bank | FR-QB-05 — A question that a Student has answered cannot be deleted | `Q_SC1` attached to `EXM_1`; `STU_A` has answered it in a submitted attempt | 1: Sign in as `FAC_A` 2: Attempt to delete `Q_SC1` 3: Inspect the attempt's stored response | `Q_SC1`, `STU_A`'s submitted attempt | Deletion refused with "This question has been attempted and cannot be deleted"; the stored response remains resolvable to the original question text | | |
| ST_005 | Question Bank | FR-QB-01, FR-QB-04, FR-QB-05 — End-to-end authoring, tagging and version-freeze | `TEST` environment; `FAC_A` assigned to `CRS_X` | 1: Sign in as `FAC_A` 2: Author three tagged questions 3: Attach them to a new examination and publish it 4: Attempt to edit one of the three 5: Confirm a new version is created and the published paper is unchanged | Three MCQs across two topics and two difficulties | Authoring and tagging succeed; once published, the paper's questions are frozen — edits produce versions rather than mutations | | |

## UC-06 — Assemble and publish an examination

Verifies `FR-EX-01`, `FR-EX-02`, `FR-EX-06`.

| Test Case ID | Name of Module | Test case description | Pre-conditions | Test Steps | Test data | Expected Results | Actual Result | Test Result |
|---|---|---|---|---|---|---|---|---|
| UT_028 | Exam Authoring | FR-EX-01 — Create an examination with all mandatory attributes | `FAC_A` signed in and assigned to `CRS_X` | 1: Open `/faculty/exams/new` 2: Enter title, course, duration, declared total marks and instructions 3: Save | Title `DBMS Unit Test 1`, course `CRS_X`, duration `60`, total `50`, instructions free text | The examination is created in **Draft** state and appears in the Faculty examination list | | |
| UT_029 | Exam Authoring | FR-EX-01 — Reject a non-positive duration | `FAC_A` signed in | 1: Open the new examination form 2: Enter a duration of zero 3: Save; repeat with a negative value | Duration `0`, then `-30` | Both rejected with "Duration must be a positive number of minutes"; no examination created | | |
| UT_030 | Exam Authoring | FR-EX-01 — Per-examination policy values persist and are read back | A Draft examination exists | 1: Open its settings 2: Enable negative marking at 0.5, enable question and option shuffling, set pass mark 40% 3: Save and reload the page | Negative `0.5`, shuffle both on, pass mark `40` | All policy values persist exactly as set and are shown unchanged after reload | | |
| UT_031 | Exam Authoring | FR-EX-01 — Reject a pass mark outside 0–100 | A Draft examination exists | 1: Open its settings 2: Enter a pass mark of 150 3: Save; repeat with −10 | Pass mark `150`, then `-10` | Both rejected with "Pass mark must be between 0 and 100"; the stored value is unchanged | | |
| UT_032 | Exam Authoring | FR-EX-06 — A Draft examination is invisible to Students | A Draft examination exists on `CRS_X`; `STU_A` enrolled in `CRS_X` | 1: Sign in as `STU_A` 2: Open the dashboard 3: Request the Draft examination's URL directly | Draft examination ID | The examination does not appear on the dashboard, and the direct request is refused with HTTP 403 or 404 | | |
| UT_033 | Exam Authoring | FR-EX-06 — Publishing moves the examination out of Draft state | A Draft examination with questions attached | 1: Open the Draft examination 2: Click Publish 3: Inspect the stored state | Draft examination with 25 questions | The state changes from `DRAFT` to `PUBLISHED`; the transition is recorded with a server timestamp | | |
| IT_015 | Exam Authoring | FR-EX-02 — Questions are attached from the bank and stored against the examination | `FAC_A` signed in; `CRS_X` bank holds at least ten questions | 1: Open a Draft examination 2: Select five questions from the bank 3: Save 4: Query the examination-question join table | Five known question IDs | Exactly the five selected questions are attached, in the chosen order, with no duplicates and no unselected question present | | |
| IT_016 | Exam Authoring | FR-EX-06 — Publishing makes the examination visible to enrolled Students only | A Draft examination on `CRS_X`; `STU_A` enrolled, `STU_B` not | 1: As `FAC_A`, publish the examination 2: Sign in as `STU_A` and check the dashboard 3: Sign in as `STU_B` and check | Published examination on `CRS_X` | `STU_A` sees it listed; `STU_B` does not, since visibility requires both publication and enrollment | | |
| ST_006 | Exam Authoring | FR-EX-01, FR-EX-02, FR-EX-06 — End-to-end paper assembly and publication | `TEST` environment; `CRS_X` bank populated; `FAC_A` assigned | 1: Sign in as `FAC_A` 2: Create a Draft with title, duration and policy values 3: Attach 25 questions from the bank 4: Confirm a Student cannot see it 5: Publish 6: Sign in as an enrolled Student and confirm the paper is listed | 60-minute paper, 25 questions, negative `0.5`, pass mark `40` | The paper is invisible while Draft, becomes visible on publication, and carries the configured policy values through unchanged | | |

## UC-07 — Schedule an examination and surface it on the Student dashboard

Verifies `FR-SCH-01`, `FR-SCH-03`.

| Test Case ID | Name of Module | Test case description | Pre-conditions | Test Steps | Test data | Expected Results | Actual Result | Test Result |
|---|---|---|---|---|---|---|---|---|
| UT_034 | Scheduling | FR-SCH-01 — Schedule a published examination with a valid window | A published examination of 60 minutes' duration exists | 1: Open the examination 2: Set window start and end date-times 3: Save | Start `2026-09-10 10:00`, end `2026-09-10 12:00` | The schedule is saved and displayed; message "Examination scheduled" | | |
| UT_035 | Scheduling | FR-SCH-01 — Reject a window whose end precedes its start | A published examination exists | 1: Set an end date-time earlier than the start 2: Save | Start `2026-09-10 12:00`, end `2026-09-10 10:00` | Rejected with "The window end must be later than the window start"; no schedule saved | | |
| UT_036 | Scheduling | FR-SCH-03 — The dashboard classifies an examination as Upcoming before its window | `STU_A` enrolled in `CRS_X`; a `CRS_X` examination scheduled to start tomorrow | 1: Sign in as `STU_A` 2: Open the dashboard 3: Locate the examination | Window starting `now + 24 h` | Listed under **Upcoming** with its start date-time; no Start button is offered | | |
| UT_037 | Scheduling | FR-SCH-03 — The dashboard classifies an examination as Live inside its window | `STU_A` enrolled; a `CRS_X` examination whose window is currently open | 1: Sign in as `STU_A` 2: Open the dashboard | Window `now − 10 min` to `now + 50 min` | Listed under **Live** with an active Start button | | |
| UT_038 | Scheduling | FR-SCH-03 — The dashboard classifies a submitted examination as Completed | `STU_A` has one submitted attempt on `EXM_1` | 1: Sign in as `STU_A` 2: Open the dashboard | `EXM_1` with a submitted attempt | Listed under **Completed**; no Start button is offered | | |
| IT_017 | Scheduling | FR-SCH-01 — The stored window is timezone-unambiguous and server-authoritative | A published examination; database inspectable | 1: Schedule a window from the UI 2: Query the stored start and end values 3: Change the client machine's timezone and reload | Start `2026-09-10 10:00 IST` | The stored values are unambiguous (UTC or with an explicit offset); the displayed window is unchanged by the client timezone switch | | |
| IT_018 | Scheduling | FR-SCH-03 — Dashboard classification is driven by server time, not the client clock | `STU_A` enrolled; a `CRS_X` examination whose window opens in one hour | 1: Sign in as `STU_A` 2: Advance the client clock by two hours 3: Reload the dashboard | Window opening at `server now + 1 h`; client clock `+2 h` | The examination remains under **Upcoming**; the tampered client clock does not promote it to Live | | |
| ST_007 | Scheduling | FR-SCH-01, FR-SCH-03 — End-to-end scheduling and dashboard transitions | `TEST` environment; a published 30-minute examination; `STU_A` enrolled | 1: As `FAC_A`, set a 60-minute window opening in two minutes 2: As `STU_A`, confirm it shows Upcoming 3: Wait for the window to open and refresh 4: Sit and submit the paper 5: Refresh the dashboard | Duration `30`, window `60 min` | The examination moves Upcoming → Live → Completed on the Student dashboard as server time advances | | |

## UC-08 — Start an attempt and receive the paper

Verifies `FR-SCH-04`, `FR-ATT-01`, `FR-ATT-02`, `FR-ATT-03`.

| Test Case ID | Name of Module | Test case description | Pre-conditions | Test Steps | Test data | Expected Results | Actual Result | Test Result |
|---|---|---|---|---|---|---|---|---|
| UT_039 | Exam Delivery | FR-SCH-04 — Starting is refused before the window opens | `STU_A` enrolled; `EXM_1` window opens in ten minutes | 1: Sign in as `STU_A` 2: Attempt to start `EXM_1` | Server time `window start − 10 min` | Refused with "This examination has not opened yet"; no attempt record is created | | |
| UT_040 | Exam Delivery | FR-SCH-04 — Starting is refused after the window closes | `STU_A` enrolled; `EXM_1` window closed one minute ago | 1: Sign in as `STU_A` 2: Attempt to start `EXM_1` | Server time `window end + 1 min` | Refused with "This examination has closed"; no attempt record is created | | |
| UT_041 | Exam Delivery | FR-SCH-04 — Starting is refused when a submitted attempt already exists | `STU_A` has one submitted attempt on `EXM_1`; the window is still open | 1: Sign in as `STU_A` 2: Attempt to start `EXM_1` again | `STU_A`, `EXM_1`, one submitted attempt | Refused with "You have already submitted this examination"; no second attempt is created | | |
| UT_042 | Exam Delivery | FR-ATT-02 — The countdown is computed from server time, not the client clock | `STU_A` has an attempt in progress on `EXM_1`, 60-minute duration, 10 minutes elapsed | 1: Note the displayed remaining time 2: Set the client clock back by 30 minutes 3: Refresh the attempt page 4: Note the remaining time again | Elapsed `10 min`; client clock moved `−30 min` | Remaining time reads approximately 50 minutes both times; the client clock change gains the candidate nothing | | |
| UT_043 | Exam Delivery | FR-ATT-03 — The palette shows the correct state for each question | `STU_A` has an attempt in progress on a 25-question paper | 1: Start the attempt and inspect question 5's palette state 2: Open question 5, answer nothing, move on, inspect again 3: Return and select an option, inspect again 4: Mark it for review and inspect again | Question 5 across four interactions | The state moves **Not Visited** → **Not Answered** → **Answered** → **Marked for Review**, matching each interaction exactly | | |
| UT_044 | Exam Delivery | FR-ATT-03 — Exactly one question is displayed at a time | `STU_A` has an attempt in progress on a 25-question paper | 1: Load the attempt screen 2: Count the question stems rendered in the DOM | 25-question paper | Exactly one stem is rendered; the other 24 are not present in the delivered markup | | |
| IT_019 | Exam Delivery | FR-ATT-01 — The attempt record is created and server-stamped before the paper is delivered | `STU_A` enrolled; `EXM_1` window open; network trace available | 1: Click Start 2: Capture the request/response sequence 3: Query the attempts table | `STU_A`, `EXM_1` | The attempt row exists with a server-generated start timestamp **before** the question payload is returned; no question data is sent if the row cannot be created | | |
| IT_020 | Exam Delivery | FR-ATT-01 — The stored start time is the server's, not the client's | `STU_A` enrolled; `EXM_1` window open | 1: Set the client clock forward by one hour 2: Start the attempt 3: Query the stored start timestamp | Client clock `+1 h` | The stored start time reflects true server time; the tampered client clock is ignored | | |
| IT_021 | Exam Delivery | FR-ATT-03 — Palette state survives navigation and reload | `STU_A` has an attempt with a mix of palette states across ten questions | 1: Produce all four states across ten questions 2: Reload the browser 3: Compare every palette state before and after | Ten questions across four states | Every state is identical after reload, because palette state is derived from server-held data rather than browser memory | | |
| ST_008 | Exam Delivery | FR-SCH-04, FR-ATT-01, FR-ATT-02, FR-ATT-03 — End-to-end paper delivery under a live window | `TEST` environment; `EXM_1` live; `STU_A` enrolled | 1: Sign in as `STU_A` 2: Confirm starting is refused before the window opens 3: Start once the window is open 4: Confirm the timer begins at the full duration and counts down 5: Navigate across several questions using the palette 6: Submit | 60-minute paper, 25 questions | The attempt starts only inside the window, the server-driven timer counts down correctly, one question shows at a time, and the palette reflects every state transition accurately | | |

## UC-09 — Autosave and resume after interruption

Verifies `FR-ATT-05`, `FR-ATT-08`.

| Test Case ID | Name of Module | Test case description | Pre-conditions | Test Steps | Test data | Expected Results | Actual Result | Test Result |
|---|---|---|---|---|---|---|---|---|
| UT_045 | Attempt Responses | FR-ATT-05 — A response is persisted without any explicit save action | `STU_A` has an attempt in progress; network trace available | 1: Select an option on question 4 2: Take no further action 3: Watch the network trace | Question 4, option A | A persistence request is sent automatically within 5 seconds of the selection; no Save button is required or present | | |
| UT_046 | Attempt Responses | FR-ATT-05 — Changing a response persists the new value, not the old | `STU_A` has answered question 3 with option B | 1: Return to question 3 2: Select option D 3: Wait six seconds 4: Query the stored response | Question 3, B replaced by D | The stored response reads option D; exactly one response is held for the question | | |
| UT_047 | Attempt Responses | FR-ATT-05 — Clearing a response persists the cleared state | `STU_A` has answered question 3 | 1: Return to question 3 2: Click Clear response 3: Wait six seconds 4: Query the stored response | Question 3, cleared | The stored response is empty and the palette returns the question to **Not Answered** | | |
| UT_048 | Attempt Responses | FR-ATT-08 — Remaining time on resume is computed from the original start | `STU_A` started `EXM_1` at server time T; 60-minute duration | 1: Note the start time 2: Wait 20 minutes 3: Reload the attempt 4: Read the remaining time | Start `T`, reload at `T + 20 min` | Remaining time reads approximately 40 minutes — derived from the original start, not reset by the reload | | |
| IT_022 | Attempt Responses | FR-ATT-05 — The autosave reaches the server inside the 5-second budget | `STU_A` has an attempt in progress; server logs timestamped | 1: Select an option and record the client-side timestamp 2: Locate the corresponding server-side write 3: Compute the difference 4: Repeat for ten selections | Ten selections across ten questions | Every response is committed server-side within 5 seconds of selection; the worst observed case is recorded | | |
| IT_023 | Attempt Responses | FR-ATT-05 — A browser crash loses no response already autosaved | `STU_A` has an attempt in progress with six questions answered | 1: Answer six questions 2: Wait six seconds 3: Kill the browser process without submitting 4: Reopen, sign in and resume | Six answered questions | All six responses are restored; nothing is lost, because persistence did not depend on submission | | |
| IT_024 | Attempt Responses | FR-ATT-08 — Resuming restores responses and does not grant extra time | `STU_A` started `EXM_1` at T; answered four questions by T + 20 min | 1: Answer four questions 2: Disconnect the network for five minutes 3: Reconnect and reopen the attempt 4: Inspect the restored answers and remaining time | Start `T`, interruption `T+20` to `T+25` | All four answers are restored; remaining time reads approximately 35 minutes, so the interruption grants no extra time | | |
| IT_025 | Attempt Responses | FR-ATT-08 — Resuming on a different device restores the same attempt state | `STU_A` has an attempt in progress on profile A with three answers | 1: Answer three questions on profile A 2: Sign in as `STU_A` on profile B 3: Open the attempt | Three answered questions; two profiles | Profile B resumes the same attempt with the three answers present and time still measured from the original start | | |
| ST_009 | Attempt Responses | FR-ATT-05, FR-ATT-08 — End-to-end answer, disconnect, resume and submit | `TEST` environment; `EXM_1` live; `STU_A` enrolled | 1: Start `EXM_1` 2: Answer five questions, changing two and clearing one 3: Disconnect for three minutes 4: Reconnect and resume 5: Verify all responses and remaining time 6: Answer the rest and submit 7: Inspect the stored attempt | 25-question paper; five answered, two changed, one cleared | Every selection, change and clear survives the interruption exactly; remaining time reflects the original start; the submitted attempt records precisely the final state of every question | | |

## UC-10 — Automatic submission on timer expiry

Verifies `FR-ATT-07`.

| Test Case ID | Name of Module | Test case description | Pre-conditions | Test Steps | Test data | Expected Results | Actual Result | Test Result |
|---|---|---|---|---|---|---|---|---|
| UT_049 | Auto-Submission | FR-ATT-07 — The attempt submits itself when remaining time reaches zero | `STU_A` has an attempt in progress with 30 seconds remaining | 1: Answer one more question 2: Take no action and let the timer run to zero 3: Observe the screen | Remaining `30 s`, then `0` | At zero the attempt is submitted automatically without any click; the Student sees "Time is up. Your paper has been submitted." | | |
| UT_050 | Auto-Submission | FR-ATT-07 — Auto-submission retains every response persisted up to that instant | `STU_A` has an attempt with eight answered questions and 20 seconds remaining | 1: Confirm eight answers 2: Let the timer expire 3: Query the submitted attempt's responses | Eight answered of 25 | All eight responses are present; the remaining 17 are recorded as unattempted | | |
| UT_051 | Auto-Submission | FR-ATT-07 — No further response is accepted after auto-submission | `STU_A`'s attempt has just auto-submitted | 1: Attempt to select an option on the last displayed question 2: Call the response-save endpoint directly with the old attempt ID | Auto-submitted attempt ID | The UI is read-only; the direct API call is refused with "This attempt has already been submitted"; the stored responses are unchanged | | |
| UT_052 | Auto-Submission | FR-ATT-07 — The attempt state becomes Submitted with a server timestamp | An attempt that has just auto-submitted | 1: Query the attempt record 2: Inspect its state and submission timestamp | Auto-submitted attempt | State reads `SUBMITTED`; the submission timestamp is server-generated and equals the attempt start plus the configured duration | | |
| IT_026 | Auto-Submission | FR-ATT-07 — Expiry is enforced server-side even if the browser is closed | `STU_A` has an attempt in progress with one minute remaining | 1: Answer two questions 2: Close the browser entirely 3: Wait until after the duration elapses 4: Sign in again and open the examination 5: Query the attempt record | Browser closed at `T − 60 s` | The attempt is recorded as submitted with the two answers retained; expiry did not depend on the browser being open | | |
| IT_027 | Auto-Submission | FR-ATT-07 — A client-side clock change cannot defer auto-submission | `STU_A` has an attempt with two minutes remaining | 1: Set the client clock back by one hour 2: Let real time pass beyond the true expiry 3: Attempt to answer a question | Client clock `−1 h`; real elapsed time beyond duration | The attempt is auto-submitted at the true server expiry; further answers are refused | | |
| IT_028 | Auto-Submission | FR-ATT-07, FR-EVL-01 — An auto-submitted attempt enters evaluation like a manual one | Auto-submission has just occurred for `STU_A` on `EXM_1` | 1: Let the attempt auto-submit 2: Query the evaluation record within 5 seconds | Auto-submitted attempt on a 25-question paper | The attempt is evaluated automatically with a total score, percentage and Pass/Fail outcome, identical in treatment to a manually submitted attempt | | |
| ST_010 | Auto-Submission | FR-ATT-07 — End-to-end timed expiry on a short paper | `TEST` environment; a 3-minute examination with five questions; `STU_A` enrolled | 1: Start the examination 2: Answer three of the five questions 3: Let the full three minutes elapse without submitting 4: Observe the screen at zero 5: Sign in as `FAC_A` and inspect the attempt | 3-minute paper, five questions, three answered | The paper submits itself exactly at expiry, the three answers are retained, the two unanswered are recorded as unattempted, and Faculty sees a normally submitted attempt | | |

## UC-11 — Evaluate a submitted attempt automatically

Verifies `FR-EVL-01`, `FR-EVL-02`, `FR-EVL-05`.

| Test Case ID | Name of Module | Test case description | Pre-conditions | Test Steps | Test data | Expected Results | Actual Result | Test Result |
|---|---|---|---|---|---|---|---|---|
| UT_053 | Evaluation | FR-EVL-02 — Award full positive marks for a correct response | Scoring engine callable in isolation; `Q_SC1` = +2 / −0.5, correct option B | 1: Invoke the evaluator with a response of option B 2: Read the awarded marks | Response `B`, correct `B`, positive `2`, negative `0.5` | The question is awarded exactly `+2.0` | | |
| UT_054 | Evaluation | FR-EVL-02 — Deduct the configured negative marks for an incorrect response | Scoring engine callable; negative marking enabled at 0.5 | 1: Invoke the evaluator with a response of option A 2: Read the awarded marks | Response `A`, correct `B`, positive `2`, negative `0.5` | The question is awarded exactly `−0.5` | | |
| UT_055 | Evaluation | FR-EVL-02 — Award zero and apply no deduction to an unattempted question | Scoring engine callable; negative marking enabled at 0.5 | 1: Invoke the evaluator with no response recorded 2: Read the awarded marks | Response `null`, correct `B`, negative `0.5` | The question is awarded exactly `0.0`; the penalty is **not** applied — the boundary that separates skipping from guessing | | |
| UT_056 | Evaluation | FR-EVL-02 — Apply no deduction when negative marking is disabled | Scoring engine callable; negative marking disabled on the examination | 1: Invoke the evaluator with an incorrect response 2: Read the awarded marks | Response `A`, correct `B`, negative marking off | The question is awarded exactly `0.0`, not a negative value | | |
| UT_057 | Evaluation | FR-EVL-05 — Compute total, percentage and a Pass outcome at the pass mark | Scoring engine callable; pass mark 40% | 1: Evaluate an attempt scoring 20 of 50 2: Read total, percentage and outcome | Total `20`, declared total `50`, pass mark `40%` | Total `20`, percentage `40.0%`, outcome **Pass** — the boundary is inclusive | | |
| UT_058 | Evaluation | FR-EVL-05 — Compute a Fail outcome just below the pass mark | Scoring engine callable; pass mark 40% | 1: Evaluate an attempt scoring 19.5 of 50 2: Read the outcome | Total `19.5`, declared total `50`, pass mark `40%` | Percentage `39.0%`, outcome **Fail** | | |
| IT_029 | Evaluation | FR-EVL-01 — Every submitted attempt is evaluated without human intervention | `EXM_1` with three submitted attempts | 1: Submit three attempts 2: Take no Faculty action of any kind 3: Query the evaluation records | Three submitted attempts | All three carry a computed score, percentage and outcome; none awaits a manual trigger or approval | | |
| IT_030 | Evaluation | FR-EVL-01, NFR-P-03 — A 100-question attempt is evaluated within 5 seconds | An examination of 100 questions with a submitted attempt; server timestamps available | 1: Submit and record the server submission timestamp 2: Poll for the evaluation record and record its completion timestamp 3: Compute the elapsed time 4: Repeat over ten attempts | 100-question paper, ten attempts | Every evaluation completes within 5 seconds of submission; the worst observed elapsed time is recorded | | |
| IT_031 | Evaluation | FR-EVL-02, FR-EVL-05 — A mixed attempt is scored correctly end to end | An examination of 10 questions at +2 / −0.5 with a submitted attempt | 1: Submit an attempt with 6 correct, 3 incorrect and 1 unattempted 2: Query the computed total, percentage and outcome | 6 correct, 3 incorrect, 1 skipped; +2 / −0.5; declared total `20`; pass mark `40%` | Total is `(6 × 2) − (3 × 0.5) − 0 = 10.5`; percentage `52.5%`; outcome **Pass**; the skipped question contributes exactly zero | | |
| ST_011 | Evaluation | FR-EVL-01, FR-EVL-02, FR-EVL-05 — End-to-end automatic scoring of a full cohort | `TEST` environment; `EXM_1` with 25 questions; five enrolled Students | 1: Have five Students sit and submit `EXM_1` with differing answer patterns 2: Take no Faculty action 3: Inspect each attempt's score, percentage and outcome 4: Hand-compute two of the five from the answer key and compare | Five attempts across a 25-question paper | All five are evaluated automatically; the two hand-computed totals match the system's exactly; Pass/Fail is correct against the configured pass mark | | |

## UC-12 — Publish results and display the scorecard

Verifies `FR-RES-01`, `FR-RES-02`, `FR-RES-03`.

| Test Case ID | Name of Module | Test case description | Pre-conditions | Test Steps | Test data | Expected Results | Actual Result | Test Result |
|---|---|---|---|---|---|---|---|---|
| UT_059 | Results | FR-RES-01 — An evaluated result is withheld until Faculty publishes | `STU_A` has a submitted, evaluated attempt on `EXM_1`; results not published | 1: Sign in as `STU_A` 2: Open the dashboard and the examination 3: Look for a score | Evaluated but unpublished result | No score, percentage or outcome is shown; the examination reads "Results not yet published" | | |
| UT_060 | Results | FR-RES-02 — Publishing makes the result visible to the Student | The situation of UT_059 | 1: Sign in as `FAC_A` 2: Publish the results of `EXM_1` 3: Sign in as `STU_A` and reopen the examination | `EXM_1` results published | The scorecard is now visible with total, percentage and outcome | | |
| UT_061 | Results | FR-RES-02 — Unpublishing withdraws a previously visible result | `EXM_1` results published and seen by `STU_A` | 1: Sign in as `FAC_A` 2: Unpublish the results 3: Sign in as `STU_A` and reopen the examination | `EXM_1` results unpublished | The scorecard is no longer shown; the examination reverts to "Results not yet published"; the stored score is unchanged | | |
| UT_062 | Results | FR-RES-03 — The scorecard shows total, percentage, outcome and per-question marks | `EXM_1` results published; `STU_A` scored 32 of 50 | 1: Sign in as `STU_A` 2: Open the scorecard 3: Inspect every displayed field | Total `32`, declared `50`, pass mark `40%`, 25 questions | Total `32`, percentage `64.0%`, outcome **Pass**, and a per-question line for all 25 questions showing the marks obtained on each | | |
| UT_063 | Results | FR-RES-03 — Per-question marks on the scorecard sum to the reported total | `EXM_1` results published for `STU_A` | 1: Open the scorecard 2: Sum the per-question marks 3: Compare with the displayed total | 25 per-question values including negatives | The sum equals the displayed total exactly | | |
| IT_032 | Results | FR-RES-01 — An unpublished result is unreachable through the API, not merely hidden in the UI | `STU_A` has an evaluated but unpublished result | 1: Sign in as `STU_A` 2: Call `GET /api/results/{attemptId}` directly 3: Inspect the response body | `STU_A`'s attempt ID; results unpublished | Refused with HTTP 403; no score, percentage or per-question mark appears anywhere in the body | | |
| IT_033 | Results | FR-RES-01 — One Student cannot read another's result | `EXM_1` results published; `STU_A` and `STU_B` both attempted | 1: Sign in as `STU_A` 2: Call the result endpoint with `STU_B`'s attempt ID | `STU_B`'s attempt ID | Refused with HTTP 403; `STU_B`'s score is not disclosed | | |
| IT_034 | Results | FR-RES-02, FR-RES-03 — The published scorecard matches the stored evaluation exactly | `EXM_1` sat by five Students and published | 1: Publish results 2: For each Student, open the scorecard 3: Compare each displayed total, percentage and outcome against the stored evaluation record | Five evaluated attempts | Every displayed figure matches its stored evaluation exactly; no rounding or transcription discrepancy | | |
| ST_012 | Results | FR-RES-01, FR-RES-02, FR-RES-03 — End-to-end publication and scorecard | `TEST` environment; `EXM_1` sat by five Students | 1: Confirm no Student can see a score before publication 2: As `FAC_A`, publish 3: As each Student, open the scorecard and verify the figures 4: Unpublish and confirm the scorecards disappear | Five evaluated attempts | Results stay hidden until published, every scorecard matches the stored evaluation, and unpublishing withdraws visibility without altering the data | | |

## UC-13 — Log integrity events and maintain the audit trail

Verifies `FR-INT-01`, `FR-INT-07`, `FR-ADM-01`.

| Test Case ID | Name of Module | Test case description | Pre-conditions | Test Steps | Test data | Expected Results | Actual Result | Test Result |
|---|---|---|---|---|---|---|---|---|
| UT_064 | Integrity | FR-INT-01 — A single focus-loss event is recorded with a timestamp | `STU_A` has an attempt in progress on `EXM_1` | 1: Switch to another browser tab once 2: Return to the attempt 3: Query the integrity event log for the attempt | One tab switch | Exactly one focus-loss event is recorded against the attempt, carrying a server-side timestamp | | |
| UT_065 | Integrity | FR-INT-01 — Repeated focus losses are each recorded separately | `STU_A` has an attempt in progress | 1: Switch away and back three times 2: Query the event log | Three tab switches | Exactly three events are recorded, each with its own distinct timestamp; none is coalesced or dropped | | |
| UT_066 | Integrity | FR-INT-01 — No event is recorded when focus is never lost | `STU_A` has an attempt in progress | 1: Complete the attempt without leaving the window 2: Query the event log | Zero tab switches | The event log for the attempt is empty; the detector does not fire on ordinary in-page interaction | | |
| UT_067 | Integrity | FR-INT-01 — The recorded timestamp is server-side, not client-supplied | `STU_A` has an attempt in progress | 1: Set the client clock forward by one hour 2: Switch tabs once 3: Query the recorded event timestamp | Client clock `+1 h`; one tab switch | The stored timestamp reflects true server time, not the tampered client clock | | |
| UT_068 | Audit | FR-ADM-01 — An audit entry records actor, action, entity, timestamp and changed values | `FAC_A` signed in; audit log inspectable | 1: Edit a question's stem 2: Query the audit log for that question | Question `Q_SC1`, stem changed | One entry exists carrying the actor `FAC_A`, the action, the affected entity, a server timestamp, and both the previous and the new stem values | | |
| IT_035 | Integrity | FR-INT-07 — No correct-answer data reaches the candidate during an active attempt | `STU_A` has an attempt in progress on `EXM_1` | 1: Capture every HTTP response delivered to the browser during the attempt 2: Search the payloads for `isCorrect`, `correctOption`, `answerKey` and the known correct values 3: Inspect the rendered HTML and client-side JavaScript state | `EXM_1`; known answer key | No response body, HTML attribute or client-side variable exposes which option is correct; the key is absent from everything the browser receives | | |
| IT_036 | Audit | FR-ADM-01 — Every mutation class writes an audit entry | `ADM_A` and `FAC_A` signed in | 1: Create a user, a course, a question and an examination, then publish a result 2: Query the audit log for each | One mutation of each of the five entity classes | An entry exists for every one of the five; no mutation class is silently unlogged | | |
| IT_037 | Audit | FR-ADM-01 — The audit log is append-only and resists modification | Audit entries exist; database reachable | 1: Attempt to update an existing audit row through the application 2: Attempt to delete one 3: Inspect the table's constraints | An existing audit entry | Both attempts are refused; the application exposes no update or delete path for audit rows; the entry is unchanged | | |
| ST_013 | Integrity & Audit | FR-INT-01, FR-INT-07, FR-ADM-01 — End-to-end evidentiary trail across an examination cycle | `TEST` environment; `EXM_1` live; `STU_A` enrolled | 1: Sit `EXM_1` as `STU_A`, switching tabs twice 2: Confirm no answer key appears in any captured payload 3: Submit 4: As `FAC_A`, publish results 5: As `ADM_A`, open the audit log filtered to `EXM_1` and reconcile it against everything that occurred | One attempt, two focus-loss events, one publication | The log accounts for every state change — attempt creation, submission, evaluation, publication — the two integrity events are attached to the attempt for Faculty review, and no answer key ever reached the candidate | | |

---

## 7. Coverage summary

| Use case | Requirements verified | Unit | Integration | System | Total |
|---|---|---|---|---|---|
| UC-01 Register a Student account | FR-AUTH-01 | 6 | 2 | 1 | 9 |
| UC-02 Sign in and role-based access | FR-AUTH-03, FR-AUTH-06 | 5 | 4 | 1 | 10 |
| UC-03 Manage courses and assign faculty | FR-CRS-01 | 5 | 2 | 1 | 8 |
| UC-04 Enroll students and gate visibility | FR-CRS-03, FR-CRS-04 | 5 | 3 | 1 | 9 |
| UC-05 Author question bank entries | FR-QB-01, FR-QB-04, FR-QB-05 | 6 | 3 | 1 | 10 |
| UC-06 Assemble and publish an examination | FR-EX-01, FR-EX-02, FR-EX-06 | 6 | 2 | 1 | 9 |
| UC-07 Schedule and surface on the dashboard | FR-SCH-01, FR-SCH-03 | 5 | 2 | 1 | 8 |
| UC-08 Start an attempt and receive the paper | FR-SCH-04, FR-ATT-01, FR-ATT-02, FR-ATT-03 | 6 | 3 | 1 | 10 |
| UC-09 Autosave and resume | FR-ATT-05, FR-ATT-08 | 4 | 4 | 1 | 9 |
| UC-10 Automatic submission on expiry | FR-ATT-07 | 4 | 3 | 1 | 8 |
| UC-11 Evaluate automatically | FR-EVL-01, FR-EVL-02, FR-EVL-05 | 6 | 3 | 1 | 10 |
| UC-12 Publish results and scorecard | FR-RES-01, FR-RES-02, FR-RES-03 | 5 | 3 | 1 | 9 |
| UC-13 Integrity events and audit trail | FR-INT-01, FR-INT-07, FR-ADM-01 | 5 | 3 | 1 | 9 |
| **Total** | **30 of 30** | **68** | **37** | **13** | **118** |

Every use case carries at least eight test cases, and every one of the 30 functional requirements of
`Documents/SRS Document.md` is exercised by at least one test case — satisfying NFR-O-05.

## 8. Open items affecting these test cases

Two decisions remain outstanding with the course instructor, and each leaves specific expected
values provisional:

| Open question | Test cases affected | Effect if resolved differently |
|---|---|---|
| Negative-marking convention — a flat deduction per wrong answer, or a fraction of the question's marks | UT_054, UT_056, IT_031 | The expected values assume a **flat** deduction of 0.5. A fractional convention changes each expected total |
| Whether a Pass at exactly the pass mark is inclusive | UT_057 | The expected outcome assumes **inclusive** — 40.0% against a 40% pass mark is a Pass |
