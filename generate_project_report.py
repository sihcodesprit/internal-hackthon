"""
Generate the complete SIH 2026 project report PDF for a 6-member team.
Team Leader receives the full document; each of the 5 members has their
own dedicated module section (SQL, Django/Python, Frontend, Testing,
Deployment & Git/GitHub).

Run: python generate_project_report.py
Output: SmartCurriculum_Team_Report.pdf
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch, mm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak,
    KeepTogether, Image
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT

OUTPUT = "SmartCurriculum_Team_Report.pdf"

DARK = colors.HexColor('#1A1A2E')
ACCENT = colors.HexColor('#6C63FF')
ACCENT2 = colors.HexColor('#00D4FF')
GREEN = colors.HexColor('#00E676')
RED = colors.HexColor('#FF5252')
AMBER = colors.HexColor('#FFD740')
BG = colors.HexColor('#F5F6FA')
ROW = colors.HexColor('#EEF0FF')

styles = getSampleStyleSheet()

# ---------------- Custom styles ----------------
cover_title = ParagraphStyle('cover_title', fontName='Helvetica-Bold', fontSize=30,
                             leading=36, textColor=colors.white, alignment=TA_CENTER, spaceAfter=10)
cover_sub = ParagraphStyle('cover_sub', fontName='Helvetica', fontSize=15,
                           leading=22, textColor=ACCENT2, alignment=TA_CENTER, spaceAfter=30)
cover_meta = ParagraphStyle('cover_meta', fontName='Helvetica', fontSize=12,
                            leading=18, textColor=colors.HexColor('#C8C8E0'),
                            alignment=TA_CENTER, spaceAfter=6)
h1 = ParagraphStyle('h1', parent=styles['Heading1'], fontName='Helvetica-Bold',
                    fontSize=17, leading=22, textColor=DARK, spaceBefore=16, spaceAfter=8,
                    borderWidth=0, borderColor=ACCENT, borderPadding=0)
h2 = ParagraphStyle('h2', parent=styles['Heading2'], fontName='Helvetica-Bold',
                    fontSize=13, leading=17, textColor=ACCENT, spaceBefore=12, spaceAfter=6)
h3 = ParagraphStyle('h3', parent=styles['Heading3'], fontName='Helvetica-Bold',
                    fontSize=11, leading=15, textColor=DARK, spaceBefore=8, spaceAfter=4)
body = ParagraphStyle('body', parent=styles['BodyText'], fontName='Helvetica',
                      fontSize=9.5, leading=14, textColor=colors.HexColor('#333333'),
                      spaceAfter=6, alignment=TA_LEFT)
bullet = ParagraphStyle('bullet', parent=body, leftIndent=14, bulletIndent=4, spaceAfter=3)
code = ParagraphStyle('code', parent=styles['Code'], fontName='Courier', fontSize=8,
                      leading=11, textColor=colors.HexColor('#1B2A4A'),
                      backColor=BG, borderPadding=6, spaceBefore=3, spaceAfter=8)
note = ParagraphStyle('note', parent=body, fontName='Helvetica-Oblique',
                      textColor=ACCENT, backColor=colors.HexColor('#F0EEFF'),
                      borderPadding=6, spaceBefore=4, spaceAfter=8)
cell_bold = ParagraphStyle('cell_bold', parent=body, fontName='Helvetica-Bold', spaceAfter=0)
cell = ParagraphStyle('cell', parent=body, fontSize=8.5, leading=11, spaceAfter=0)
cell_code = ParagraphStyle('cell_code', parent=cell, fontName='Courier', fontSize=8, leading=10)
kpi_num = ParagraphStyle('kpi_num', parent=body, fontName='Helvetica-Bold', fontSize=14,
                         textColor=ACCENT, alignment=TA_CENTER, spaceAfter=0)
kpi_lab = ParagraphStyle('kpi_lab', parent=body, fontSize=8, textColor=colors.HexColor('#666688'),
                         alignment=TA_CENTER, spaceAfter=0)


def H1(text):
    return [Spacer(1, 6), Paragraph(text, h1), Spacer(1, 4)]


def H2(text):
    return [Paragraph(text, h2)]


def H3(text):
    return [Paragraph(text, h3)]


def P(text, style=body):
    return [Paragraph(text, style)]


def B(text):
    return [Paragraph(text, bullet)]


def CODE(lines):
    if isinstance(lines, str):
        lines = lines.split('\n')
    return [Paragraph('<br/>'.join(line.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                                  .replace(' ', '&nbsp;') for line in lines), code)]


def make_table(data, widths, header=True):
    rows = []
    if header:
        header_row = [Paragraph(f'<b>{c}</b>', cell_bold) for c in data[0]]
        rows.append(header_row)
        for r in data[1:]:
            rows.append([Paragraph(str(c), cell) for c in r])
        t = Table(rows, colWidths=widths, repeatRows=1)
    else:
        for r in data:
            rows.append([Paragraph(str(c), cell) for c in r])
        t = Table(rows, colWidths=widths)
    style = [
        ('BACKGROUND', (0, 0), (-1, 0), DARK) if header else ('BACKGROUND', (0, 0), (-1, -1), ROW),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white) if header else [],
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, ROW]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CCCCDD')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]
    flat = []
    for s in style:
        if s:
            flat.append(s)
    t.setStyle(TableStyle(flat))
    return t


def kpi_row(items):
    cols = []
    for v, l in items:
        cols.append([Paragraph(v, kpi_num), Paragraph(l, kpi_lab)])
    t = Table(cols, colWidths=[(190 * mm) / len(items)] * len(items))
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), ROW),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#CCCCDD')),
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.HexColor('#CCCCDD')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    return t


def section_cover(num, title, member, color, desc):
    el = [PageBreak()]
    band = Table([[Paragraph(f'<font color="white"><b>{num}</b></font>', ParagraphStyle(
        'num', parent=body, fontName='Helvetica-Bold', fontSize=26, textColor=colors.white,
        alignment=TA_LEFT))]], colWidths=[40 * mm], rowHeights=[16 * mm])
    band.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), color),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
    ]))
    el.append(band)
    el.append(Spacer(1, 10))
    el.append(Paragraph(title, ParagraphStyle('t', parent=h1, fontSize=20, leading=26, textColor=DARK)))
    el.append(Spacer(1, 4))
    el.append(Paragraph(member, ParagraphStyle('m', parent=body, fontName='Helvetica-Bold',
                                               fontSize=12, textColor=ACCENT, spaceAfter=8)))
    el.append(Paragraph(desc, body))
    el.append(Spacer(1, 6))
    return el


story = []

# =====================================================================
# COVER PAGE  (drawn on the first page canvas)
# =====================================================================
def draw_cover(canvas, doc_):
    canvas.saveState()
    canvas.setFillColor(DARK)
    canvas.rect(0, 0, A4[0], A4[1], stroke=0, fill=1)
    canvas.setFillColor(colors.HexColor('#6C63FF'))
    canvas.rect(0, A4[1] - 6 * mm, A4[0], 6 * mm, stroke=0, fill=1)
    canvas.setFillColor(colors.HexColor('#00D4FF'))
    canvas.rect(0, 6 * mm, A4[0], 2 * mm, stroke=0, fill=1)
    w, h = A4
    canvas.setFillColor(colors.white)
    canvas.setFont('Helvetica-Bold', 34)
    canvas.drawCentredString(w / 2, h - 150, 'SMART CURRICULUM')
    canvas.setFillColor(ACCENT2)
    canvas.setFont('Helvetica', 16)
    canvas.drawCentredString(w / 2, h - 175, 'Activity & Attendance System')
    canvas.setFillColor(colors.HexColor('#C8C8E0'))
    canvas.setFont('Helvetica', 12)
    canvas.drawCentredString(w / 2, h - 215, 'Full Project Report & Team Handbook')
    canvas.setStrokeColor(colors.HexColor('#6C63FF'))
    canvas.setLineWidth(1)
    canvas.line(w / 2 - 70, h - 230, w / 2 + 70, h - 230)
    canvas.setFillColor(colors.white)
    canvas.setFont('Helvetica-Bold', 14)
    canvas.drawCentredString(w / 2, h - 290, 'Smart India Hackathon (SIH) 2026 - Internal Round')
    canvas.setFont('Helvetica', 12)
    canvas.drawCentredString(w / 2, h - 315, 'Team of 6  |  1 Team Leader + 5 Module Leads')
    canvas.drawCentredString(w / 2, h - 335, 'Role-Based Technical Documentation')
    canvas.drawCentredString(w / 2, h - 365, 'Complete system knowledge for the Team Leader, with dedicated module')
    canvas.drawCentredString(w / 2, h - 385, 'sections for Database, Backend, Frontend, Testing and Deployment / Git & GitHub.')
    canvas.setFillColor(ACCENT2)
    canvas.setFont('Helvetica-Bold', 11)
    canvas.drawCentredString(w / 2, 45, 'Team SmartCurriculum - Internal Hackathon 2026')
    canvas.restoreState()

story.append(Spacer(1, 1))
story.append(PageBreak())

# =====================================================================
# TABLE OF CONTENTS
# =====================================================================
story += H1('Table of Contents')
toc = [
    ('0.', 'Team Structure &amp; Role Assignments', 'All'),
    ('1.', 'Project Overview (Problem, Solution, Features)', 'Team Leader'),
    ('2.', 'System Architecture &amp; Module Connections', 'Team Leader'),
    ('3.', 'Database Design &amp; SQL', 'Member 1 - SQL'),
    ('4.', 'Backend - Python &amp; Django', 'Member 2 - Django'),
    ('5.', 'Frontend Technology Stack', 'Member 3 - Frontend'),
    ('6.', 'Testing Strategy', 'Member 4 - Testing'),
    ('7.', 'Deployment, Git &amp; GitHub', 'Member 5 - DevOps'),
    ('8.', 'Demo Data, Credentials &amp; Run Guide', 'Team Leader'),
    ('9.', 'Conclusion &amp; Future Roadmap', 'Team Leader'),
]
story.append(make_table(
    [('Section', 'Topic', 'Primary Owner')] +
    [[a, b, c] for a, b, c in toc],
    [22 * mm, 108 * mm, 60 * mm]
))
story.append(Spacer(1, 12))
story.append(Paragraph(
    '<b>How to use this handbook:</b> The Team Leader is expected to know Sections 0-9 fully and '
    'can answer questions across all modules. Each of the 5 members is primarily responsible for '
    'their numbered section but must understand how it connects to the rest of the system.', note))

# =====================================================================
# SECTION 0 - TEAM STRUCTURE
# =====================================================================
story += section_cover('0', 'Team Structure &amp; Role Assignments', 'Applies to all 6 members',
                       DARK, 'The project is split into 6 clear work streams. Every member owns one '
                             'module end-to-end while the Team Leader holds the complete picture.')
story += H2('Role Matrix')
story.append(make_table(
    [('Member', 'Role', 'Responsible For', 'Knows (Scope)')] +
    [
        ['Team Leader', 'Project Lead / Architect', 'Everything: architecture, connections, data flow, integration, reviews, final submission', 'Full system (Sections 1-8)'],
        ['Member 1', 'Database Engineer', 'Data models, SQL, migrations, relationships, queries, seed data', 'SQL + schema (Section 3)'],
        ['Member 2', 'Backend Engineer', 'Django apps, views, URLs, DRF APIs, forms, authentication, business logic', 'Python / Django (Section 4)'],
        ['Member 3', 'Frontend Engineer', 'HTML templates, CSS theme, JS interactivity, QR scanner, charts', 'Frontend stack (Section 5)'],
        ['Member 4', 'QA / Testing Engineer', 'Test plan, unit &amp; integration tests, bug reports, regression', 'Testing (Section 6)'],
        ['Member 5', 'DevOps Engineer', 'Git workflow, GitHub, Vercel deployment, env config, builds', 'Deployment + Git/GitHub (Section 7)'],
    ],
    [24 * mm, 32 * mm, 64 * mm, 70 * mm]
))
story += H2('Team Communication Rules')
for b in [
    '<b>Knowledge boundary:</b> Every member masters their own module but must explain how it connects to the others (they need not know every implementation detail of other modules).',
    '<b>Team Leader ownership:</b> The leader is the single point of truth for architecture decisions, integrations, and the final presentation.',
    '<b>Code flow:</b> All code merges through the Team Leader\u2019s review before going to the main branch on GitHub.',
    '<b>Demo responsibility:</b> Each member presents their own module at the internal round.',
]:
    story += B(b)

# =====================================================================
# SECTION 1 - PROJECT OVERVIEW
# =====================================================================
story += section_cover('1', 'Project Overview', 'Team Leader - must know everything',
                       ACCENT, 'What the product is, the problem it solves, and the feature set.')
story += H2('1.1 Executive Summary')
story += P(
    'SmartCurriculum Activity &amp; Attendance is a Django-based web application that removes classroom '
    'administration overhead while turning students\u2019 empty periods into productive study time. Teachers '
    'generate a time-limited QR code for each class; students scan it to mark attendance in under a second. '
    'A timetable engine then detects free periods and a daily planner auto-suggests subject-linked tasks, '
    'so every free slot becomes active learning. Analytics dashboards give both teachers and students '
    'live, chart-driven insight into attendance performance.')
story += H2('1.2 Problem Statement')
for b in [
    'Manual roll-call wastes 3-5 minutes of every class and is prone to proxy attendance.',
    'Students do not know their attendance percentage until it is too late (75% rule).',
    'Empty periods are wasted; there is no system to guide students toward productive work.',
    'Teachers lack an automated way to monitor low-attendance students and export reports.',
]:
    story += B(b)
story += H2('1.3 Our Solution')
for b in [
    '<b>QR-based attendance:</b> UUID sessions with expiry countdowns; one scan per student per session.',
    '<b>Free-period optimizer:</b> Timetable parser detects free slots and the planner recommends tasks filtered by the student\u2019s enrolled subjects.',
    '<b>Analytics:</b> Daily trends, per-subject percentages, 75% threshold warning flags (safe / warning / danger).',
    '<b>Exports:</b> One-click Excel and PDF attendance reports per session.',
]:
    story += B(b)
story += H2('1.4 Feature List &amp; Tech Snapshot')
story.append(kpi_row([
    ('4', 'Django Apps'),
    ('8', 'Database Tables'),
    ('4', 'REST API Endpoints'),
    ('6', 'Team Members'),
    ('75%', 'Attendance Rule'),
]))
story.append(Spacer(1, 10))
story.append(make_table(
    [('Layer', 'Technology', 'Version / Tool')] +
    [
        ['Backend Framework', 'Django', '5.2+'],
        ['REST API', 'Django REST Framework', '3.16+'],
        ['Database (dev)', 'SQLite', 'bundled with Python'],
        ['Database (prod)', 'PostgreSQL (serverless)', 'Neon Postgres via DATABASE_URL'],
        ['ORM / SQL', 'Django ORM + Raw SQL support', 'sqlite3 / psycopg (psycopg[binary])'],
        ['Frontend', 'HTML / CSS / JavaScript', 'Bootstrap 5.3, Chart.js 4.4, jsQR 1.4'],
        ['PDF Reports', 'ReportLab', '4.4+'],
        ['Excel Reports', 'openpyxl', 'via pip'],
        ['QR Generation', 'qrcode + Pillow', '8.0+'],
        ['Deployment', 'Vercel (Serverless Python)', 'vercel.json'],
        ['Version Control', 'Git + GitHub', 'main branch workflow'],
    ],
    [48 * mm, 80 * mm, 62 * mm]
))

# =====================================================================
# SECTION 2 - ARCHITECTURE & CONNECTIONS
# =====================================================================
story += section_cover('2', 'System Architecture &amp; Module Connections',
                       'Team Leader - must know everything', ACCENT,
                       'How the 4 Django apps connect to each other, the full request flow, and the '
                       'URL routing map. This is the integration blueprint of the project.')
story += H2('2.1 High-Level Architecture')
story.append(make_table(
    [('Layer', 'What Lives Here')] +
    [
        ['Client', 'Browser (teacher / student). Bootstraps Bootstrap 5.3, Chart.js, jsQR via CDN.'],
        ['Web Server', 'Django WSGI (local dev) or Vercel serverless Python runtime (production).'],
        ['Routing', 'smartcurriculum/urls.py includes accounts, attendance, timetable, analytics and the /api/ endpoints.'],
        ['Application Layer', 'accounts (users/roles), attendance (QR sessions &amp; records), timetable (slots &amp; planner), analytics (aggregation views).'],
        ['Database Layer', 'SQLite locally, PostgreSQL on Vercel. Accessed only through the Django ORM.'],
        ['Static / Media', 'static/ (CSS, JS) served by WhiteNoise-equivalent; media/ stores QR PNGs and profile pictures.'],
    ],
    [40 * mm, 150 * mm]
))
story += H2('2.2 App-to-App Connections (Data Flow)')
story.append(make_table(
    [('From', 'To', 'Connection', 'How')] +
    [
        ['accounts.CustomUser', 'attendance.Class', 'teacher (FK) + students (M2M)', 'Class.teacher -> teacher user; Class.students -> student users'],
        ['attendance.Subject', 'attendance.Class', 'subject (FK)', 'Each class is a specific subject offering'],
        ['attendance.Class', 'attendance.AttendanceSession', 'class_obj (FK)', 'A session is one attendance window for a class'],
        ['attendance.AttendanceSession', 'attendance.AttendanceRecord', 'session (FK)', 'Every scan creates one record per student'],
        ['accounts.CustomUser', 'attendance.AttendanceRecord', 'student (FK)', 'Tracks which student was present/late'],
        ['attendance.Class', 'timetable.TimeSlot', 'class_obj (FK)', 'Timetable slots reference class objects'],
        ['timetable.TaskSuggestion', 'timetable.DailyPlanner', 'tasks (M2M)', 'Planner auto-picks tasks by student\u2019s subjects'],
        ['accounts.CustomUser', 'timetable.DailyPlanner', 'student (FK)', 'One planner per student per day'],
        ['attendance.*', 'analytics.views', 'read-only queries', 'Analytics aggregates sessions &amp; records via ORM'],
    ],
    [34 * mm, 36 * mm, 40 * mm, 80 * mm]
))
story += H2('2.3 URL Routing Map')
story.append(make_table(
    [('URL Pattern', 'View', 'Access')] +
    [
        ['/accounts/login/ , /logout/ , /register/student/ , /register/teacher/ , /profile/', 'accounts.views', 'Public (login/register), login (profile)'],
        ['/ (dashboard)', 'attendance.views.dashboard', 'Any authenticated user'],
        ['/classes/ , /classes/create/ , /classes/&lt;id&gt;/', 'attendance.views.class_*', 'Teacher/student'],
        ['/classes/&lt;id&gt;/generate-qr/', 'attendance.views.generate_qr', 'Teacher only'],
        ['/attendance/mark/', 'attendance.views.mark_attendance', 'Student only'],
        ['/attendance/history/', 'attendance.views.attendance_history', 'Any'],
        ['/attendance/session/&lt;uuid&gt;/ (+ close/export)', 'attendance.views.session_detail etc.', 'Teacher (close), any (view)'],
        ['/timetable/ , /timetable/planner/', 'timetable.views.timetable_view, daily_planner', 'Student / teacher'],
        ['/analytics/', 'analytics.views.analytics_dashboard', 'Any'],
        ['/api/mark-attendance/', 'api_views.api_mark_attendance', 'Student (session auth)'],
        ['/api/session/&lt;uuid&gt;/status/', 'api_views.api_session_status', 'Authenticated'],
        ['/api/student/attendance/', 'api_views.api_student_attendance', 'Student'],
        ['/api/student/active-sessions/', 'api_views.api_active_sessions', 'Student'],
    ],
    [62 * mm, 58 * mm, 70 * mm]
))
story += H2('2.4 Core Business Flow')
for step, txt in [
    ('1', 'Teacher creates a Class (ClassForm) and picks the Subject and enrolled Students.'),
    ('2', 'Teacher opens the class and clicks <b>Generate QR</b> -> AttendanceSession created with status=active, UUID session_id and expires_at = now + duration (default 15 min).'),
    ('3', 'A QR PNG is generated from the JSON payload {session_id, class, subject, timestamp} and saved to media/.'),
    ('4', 'Student scans (camera via jsQR, file upload, or manual paste) -> POST /attendance/mark/ with the session JSON.'),
    ('5', 'mark_attendance validates session activity + enrolment, then AttendanceRecord is created (unique per session+student).'),
    ('6', 'Session expires automatically (is_active() flips status to expired). Teacher can close it early.'),
    ('7', 'Attendance history, session detail, Excel/PDF export, and analytics all read from AttendanceRecord.'),
    ('8', 'Timetable finds today\u2019s free periods -> DailyPlanner auto-fills tasks from TaskSuggestion linked to enrolled subjects.'),
]:
    story += B(f'<b>Step {step}:</b> {txt}')
story += H2('2.5 Authentication &amp; Roles')
for b in [
    '<b>CustomUser (accounts.CustomUser)</b> extends Django AbstractUser with role (student / teacher / admin), phone, department, roll_number, employee_id, year_of_study, section and profile_picture.',
    '<b>Login:</b> Session-based (DRF SessionAuthentication + Django auth). Session cookie valid 24 hours.',
    '<b>Role guards:</b> is_teacher() / is_student() checked in views; API endpoints return 403 for wrong roles.',
    '<b>Security:</b> CSRF enforced on POST forms; QR payloads carry no secrets, only a UUID.',
]:
    story += B(b)

# =====================================================================
# SECTION 3 - DATABASE & SQL  (Member 1)
# =====================================================================
story += section_cover('3', 'Database Design &amp; SQL', 'Member 1 - Database Engineer',
                       GREEN, 'Complete schema, table columns, relationships, database configuration '
                             'and the SQL / ORM queries used by the application.')
story += H2('3.1 Database Configuration')
story += P(
    'Located in <b>smartcurriculum/settings.py</b>. Development uses SQLite (zero setup). In production, '
    'the app automatically switches to PostgreSQL when a DATABASE_URL / POSTGRES_URL environment variable '
    'is present (parsed by dj-database-url with conn_max_age=600 for connection pooling). The Postgres '
    'driver psycopg[binary] is declared in requirements.txt. On Vercel the build runs migrate + seed_data '
    'automatically, so the production schema and demo users are created at deploy time.')
story += CODE([
    'db_url = os.environ.get(\'DATABASE_URL\') or os.environ.get(\'POSTGRES_URL\')',
    '        or os.environ.get(\'POSTGRES_URL_NON_POOLING\')',
    'if db_url:',
    '    DATABASES = {\'default\': dj_database_url.parse(db_url, conn_max_age=600)}',
    'else:',
    '    DATABASES = {\'default\': {\'ENGINE\': \'django.db.backends.sqlite3\',',
    '                 \'NAME\': BASE_DIR / \'db.sqlite3\'}}',
])
story += H2('3.2 Table Inventory (8 Tables)')
story.append(make_table(
    [('Table', 'Purpose', 'Key Columns')] +
    [
        ['accounts_customuser', 'Users of all roles', 'username, password, first_name, last_name, email, role, phone, department, roll_number, employee_id, year_of_study, section, profile_picture'],
        ['attendance_subject', 'Academic subjects', 'name, code (unique), department, credits'],
        ['attendance_class', 'Class offering (teacher + students + subject)', 'name, department, year, section, subject_id (FK), teacher_id (FK), students (M2M)'],
        ['attendance_attendancesession', 'One QR attendance window', 'session_id (UUID unique), class_obj_id (FK), teacher_id (FK), date, start_time, end_time, status, expires_at, qr_code, qr_data, location'],
        ['attendance_attendancerecord', 'Per-student scan result', 'session_id (FK), student_id (FK), status, marked_at, ip_address, device_info, latitude, longitude'],
        ['timetable_timeslot', 'Weekly schedule', 'class_obj_id (FK), day, start_time, end_time, slot_type, room_number, department, year, section'],
        ['timetable_tasksuggestion', 'Prebuilt study tasks', 'title, description, category, subject_id (FK), duration_minutes, priority, resources_link'],
        ['timetable_dailyplanner', 'Per-student daily planner', 'student_id (FK), date, custom_notes, tasks (M2M), completed_tasks (M2M)'],
    ],
    [52 * mm, 42 * mm, 96 * mm]
))
story += H2('3.3 Relationships &amp; Constraints')
for b in [
    '<b>One-to-Many:</b> Subject -> Class -> AttendanceSession -> AttendanceRecord (CASCADE delete).',
    '<b>One-to-Many:</b> Teacher (CustomUser) -> Class (teaching_classes), Teacher -> AttendanceSession (created_sessions), Student -> AttendanceRecord.',
    '<b>Many-to-Many:</b> Class.students (enrolled students); DailyPlanner.tasks and DailyPlanner.completed_tasks (both to TaskSuggestion).',
    '<b>Unique constraints:</b> Subject.code unique; AttendanceRecord unique_together (session, student) -> a student cannot mark twice; DailyPlanner unique_together (student, date).',
    '<b>Role restrictions:</b> Class.teacher limited to role=teacher; Class.students limited to role=student (limit_choices_to).',
]:
    story += B(b)
story += H2('3.4 Status &amp; Choice Fields (enum-like)')
story.append(make_table(
    [('Field', 'Choices', 'Meaning')] +
    [
        ['CustomUser.role', 'student, teacher, admin', 'Drives dashboard routing and view permissions'],
        ['AttendanceSession.status', 'active, expired, closed', 'Lifecycle of a QR window'],
        ['AttendanceRecord.status', 'present, absent, late', 'Outcome of a scan / manual marking'],
        ['TimeSlot.day', 'MON..SAT', 'Day of the week'],
        ['TimeSlot.slot_type', 'class, free, lunch, lab', 'Enables free-period detection'],
        ['TaskSuggestion.category', 'study, revision, assignment, project, reading, practice, research', 'Classifies suggested tasks'],
    ],
    [52 * mm, 62 * mm, 76 * mm]
))
story += H2('3.5 Key Queries Used in the App (ORML &amp; SQL Equivalent)')
story += H3('3.5.1 Attendance percentage per subject (student dashboard)')
story += CODE([
    'total_sessions = AttendanceSession.objects.filter(class_obj=cls).count()',
    'present_count = AttendanceRecord.objects.filter(',
    '    student=student, session__class_obj=cls, status=\'present\').count()',
    'percentage = round((present_count / total_sessions * 100), 1)',
    '',
    '# SQL:',
    '# SELECT COUNT(*) FROM attendance_attendancesession',
    '#   WHERE class_obj_id = <cls.id>;',
    '# SELECT COUNT(*) FROM attendance_attendancerecord r',
    '#   JOIN attendance_attendancesession s ON r.session_id = s.id',
    '#   WHERE r.student_id = <sid> AND s.class_obj_id = <cid>',
    '#     AND r.status = \'present\';',
])
story += H3('3.5.2 Detect absent students for a session')
story += CODE([
    'absent_students = session.class_obj.students.exclude(',
    '    attendance_records__session=session)',
    '',
    '# SQL (simplified):',
    '# SELECT u.* FROM accounts_customuser u',
    '#   JOIN attendance_class_students cs ON u.id = cs.customuser_id',
    '#   WHERE cs.class_id = <cid>',
    '#     AND u.id NOT IN (',
    '#        SELECT student_id FROM attendance_attendancerecord',
    '#         WHERE session_id = <sid>);',
])
story += H3('3.5.3 Active sessions a student has not yet marked')
story += CODE([
    'AttendanceSession.objects.filter(class_obj__in=enrolled, status=\'active\')',
    '    .exclude(records__student=request.user)',
])
story += H2('3.6 Migrations &amp; Seeding')
for b in [
    '<b>Create/apply migrations:</b> python manage.py makemigrations &amp;&amp; python manage.py migrate',
    '<b>Seed demo data:</b> python manage.py seed_data  (creates admin, 3 teachers, 8 students, 5 subjects, 4 classes, 10 days of sessions/records, timetable, 10 tasks)',
    '<b>Idempotent:</b> seed_data uses get_or_create so it can be re-run safely (important for Vercel build).',
]:
    story += B(b)

# =====================================================================
# SECTION 4 - BACKEND DJANGO  (Member 2)
# =====================================================================
story += section_cover('4', 'Backend - Python &amp; Django', 'Member 2 - Backend Engineer',
                       ACCENT2, 'Project layout, settings, apps, views, URL wiring, DRF API, forms, '
                                'admin and authentication logic.')
story += H2('4.1 Project Layout')
story += CODE([
    'internal-hackthon/',
    '  manage.py                 # Django CLI entry point',
    '  smartcurriculum/          # Project config package',
    '      settings.py           # Apps, DB, auth, templates, static, CORS, DRF',
    '      urls.py               # Root URLconf (includes all apps + api)',
    '      asgi.py / wsgi.py     # ASGI / WSGI entry points',
    '  accounts/                 # CustomUser + registration/login/profile',
    '  attendance/               # Subjects, Classes, Sessions, Records + API',
    '  timetable/                # TimeSlots, TaskSuggestions, DailyPlanner',
    '  analytics/                # Teacher & student analytics dashboards',
    '  templates/                # All HTML templates (base + per-app)',
    '  static/                   # css/main.css, js/main.js',
    '  media/                    # Uploaded QR codes + profile pictures',
    '  attendance/management/commands/seed_data.py',
    '  requirements.txt          # Python dependencies',
    '  vercel.json               # Vercel build/deploy config',
])
story += H2('4.2 settings.py Highlights')
for b in [
    '<b>INSTALLED_APPS:</b> django.contrib.* + rest_framework, corsheaders, crispy_forms, crispy_bootstrap5, accounts, attendance, timetable, analytics.',
    '<b>AUTH_USER_MODEL</b> = accounts.CustomUser (custom user model, set before first migration).',
    '<b>DRF:</b> SessionAuthentication; default permission IsAuthenticated.',
    '<b>CORS:</b> CORS_ALLOW_ALL_ORIGINS=True (prototype); CSRF_TRUSTED_ORIGINS read from env.',
    '<b>Static/Media:</b> STATIC_URL=/static/, STATIC_ROOT=staticfiles, MEDIA_ROOT=media, MEDIA_URL=/media/ served via static() helper in urls.py.',
    '<b>Time zone:</b> Asia/Kolkata; SESSION_COOKIE_AGE = 86400 (24 h).',
]:
    story += B(b)
story += H2('4.3 Apps, Views &amp; URL Patterns')
story += H3('4.3.1 accounts')
story.append(make_table(
    [('View', 'Purpose')] +
    [
        ['login_view', 'AuthenticationForm; redirects by next= or dashboard'],
        ['logout_view', 'Logs out and redirects to login'],
        ['register_student / register_teacher', 'Role-based UserCreationForm; auto-login after save'],
        ['profile_view', 'ProfileUpdateForm incl. profile picture upload'],
    ],
    [70 * mm, 120 * mm]
))
story += H3('4.3.2 attendance (core)')
story.append(make_table(
    [('View', 'Purpose')] +
    [
        ['dashboard', 'Routes teacher / student / admin to their dashboard'],
        ['teacher_dashboard', 'Classes, today\u2019s + active sessions, student count'],
        ['student_dashboard', 'Enrolled classes, per-subject %, recent records, active sessions to scan'],
        ['class_list / class_create / class_detail', 'CRUD-lite for classes incl. per-student stats'],
        ['generate_qr', 'Creates active session, JSON payload, saves QR PNG (qrcode + Pillow)'],
        ['mark_attendance', 'Parses QR JSON, validates session + enrolment, creates record (JSON response)'],
        ['session_detail / close_session', 'Live attendance view; teacher closes early'],
        ['attendance_history', 'Teacher session list / student record list'],
        ['export_attendance_excel', 'openpyxl workbook download'],
        ['export_attendance_pdf', 'ReportLab PDF download (A4 table report)'],
    ],
    [62 * mm, 128 * mm]
))
story += H3('4.3.3 timetable')
story.append(make_table(
    [('View', 'Purpose')] +
    [
        ['timetable_view', 'Grid (MON-SAT) of TimeSlots; today\u2019s slots + free periods'],
        ['daily_planner', 'Auto-suggests tasks from enrolled subjects; marks completed; notes'],
    ],
    [55 * mm, 135 * mm]
))
story += H3('4.3.4 analytics')
story.append(make_table(
    [('View', 'Purpose')] +
    [
        ['teacher_analytics', '14-day trend, class summary, low-attendance (&lt;75%) warning list'],
        ['student_analytics', 'Per-subject %, needed-for-75% counter, 30-day trend, overall stats'],
    ],
    [55 * mm, 135 * mm]
))
story += H2('4.4 REST API (Django REST Framework)')
story.append(make_table(
    [('Method', 'Endpoint', 'Body / Params', 'Response')] +
    [
        ['POST', '/api/mark-attendance/', 'session_id (QR JSON or UUID)', '{success, message}'],
        ['GET', '/api/session/&lt;uuid&gt;/status/', '-', 'session + records + present_count + total_students'],
        ['GET', '/api/student/attendance/', '-', 'list of attendance records'],
        ['GET', '/api/student/active-sessions/', '-', 'list of active scannable sessions'],
    ],
    [22 * mm, 52 * mm, 48 * mm, 68 * mm]
))
story += H2('4.5 Forms &amp; Admin')
for b in [
    '<b>ClassForm:</b> fields name/department/year/section/subject/students; students queryset filtered to role=student.',
    '<b>AttendanceSessionForm:</b> location + duration (5-120 min).',
    '<b>Student/Teacher RegistrationForm:</b> UserCreationForm subclasses that stamp role on save.',
    '<b>Admin:</b> All 8 models registered with list_display / filters / search; CustomUser uses fieldsets.',
]:
    story += B(b)

# =====================================================================
# SECTION 5 - FRONTEND  (Member 3)
# =====================================================================
story += section_cover('5', 'Frontend Technology Stack', 'Member 3 - Frontend Engineer',
                       AMBER, 'Templates, styling system, JavaScript behaviour, QR scanning UX and '
                              'chart rendering.')
story += H2('5.1 Stack Summary')
story.append(make_table(
    [('Asset', 'Tech', 'Source / Notes')] +
    [
        ['Templates', 'Django Template Language (DTL)', 'templates/ with base.html + extends/blocks'],
        ['CSS Framework', 'Bootstrap 5.3.0', 'CDN (jsdelivr)'],
        ['Icons', 'Font Awesome 6.5.0', 'CDN (cloudflare)'],
        ['Fonts', 'Inter + Space Grotesk', 'Google Fonts'],
        ['Charts', 'Chart.js 4.4.0', 'CDN; line / doughnut / bar'],
        ['QR Scanning', 'jsQR 1.4.0', 'CDN; camera + image + manual input'],
        ['Custom CSS', 'static/css/main.css', 'Dark/light themes via CSS variables'],
        ['Custom JS', 'static/js/main.js', 'Theme, sidebar, scanner, toasts, charts, countdown'],
    ],
    [40 * mm, 52 * mm, 98 * mm]
))
story += H2('5.2 Template Architecture')
for b in [
    '<b>base.html</b> holds the responsive sidebar (role-aware nav links), topbar (clock, theme toggle, bell), messages area and content block. Loads Bootstrap bundle, Chart.js and main.js.',
    '<b>Blocks:</b> title, extra_css, breadcrumb, content, extra_js allow every page to extend base cleanly.',
    '<b>Role-aware navigation:</b> teachers see My Classes / Create Class / Attendance History; students see Scan QR / My Classes / My Attendance / Timetable / Daily Planner.',
    '<b>Theme:</b> <html data-theme="dark|light">; CSS variables (--bg-card, --text-primary, --accent-primary, ...) redefine all colours per theme; choice stored in localStorage.',
]:
    story += B(b)
story += H2('5.3 JavaScript Features (main.js)')
story.append(make_table(
    [('Feature', 'Function(s)', 'Behaviour')] +
    [
        ['Theme toggle', 'applyTheme / toggleTheme', 'Swaps data-theme + icon; persisted in localStorage'],
        ['Sidebar', 'toggleSidebar', 'Collapse on desktop, overlay drawer on mobile'],
        ['Live clock', 'updateClock', 'IST time updated every second in topbar'],
        ['Counters', 'animateCounters', 'Eased count-up on [data-count] cards'],
        ['Progress bars', 'animateProgressBars', 'Width animation via [data-progress]'],
        ['Toasts', 'showToast', 'Stacked success/error notifications'],
        ['QR camera scan', 'startQRScanner / scanFrame / stopQRScanner', 'getUserMedia video -> jsQR decode -> submit'],
        ['QR image scan', 'handleQRDrop / handleQRFileSelect / scanQRImage', 'Drag-drop or file picker -> jsQR decode'],
        ['Manual submit', 'submitManualQR / submitAttendance', 'POSTs session data to /attendance/mark/'],
        ['Session countdown', 'startCountdown', 'Live expiry timer on the QR display page'],
        ['Live refresh', 'autoRefreshSession', 'Polls /api/session/&lt;uuid&gt;/status/ every 5s'],
        ['Charts', 'createDonutChart / createLineChart / createBarChart', 'Chart.js renderers for analytics'],
        ['Copy link', 'copyShareLink', 'Copies QR share URL to clipboard'],
    ],
    [38 * mm, 52 * mm, 100 * mm]
))
story += H2('5.4 Mark Attendance UX (mark_attendance.html)')
for b in [
    '<b>Camera:</b> <video id="qrVideo"> + hidden <canvas>; jsQR decodes each frame; on hit, stops stream and posts immediately.',
    '<b>Drag &amp; drop / browse:</b> dropzone accepts image/*; decoded via jsQR on a canvas.',
    '<b>Manual input:</b> paste the raw QR JSON or UUID, then Submit.',
    '<b>Success overlay:</b> full-screen overlay with animated check on success.',
    '<b>Deep-link support:</b> /attendance/mark/?session_id=...&amp;class=...&amp;subject=... pre-fills the input and shows class details.',
]:
    story += B(b)

# =====================================================================
# SECTION 6 - TESTING  (Member 4)
# =====================================================================
story += section_cover('6', 'Testing Strategy', 'Member 4 - QA / Testing Engineer',
                       RED, 'Test framework, what to cover, how to run tests, and the QA checklist '
                            'for the demo.')
story += H2('6.1 Framework &amp; Tooling')
for b in [
    '<b>Framework:</b> Django\u2019s built-in unittest (django.test.TestCase / Client). No extra test library required.',
    '<b>API tests:</b> DRF\u2019s APIClient for endpoint-level checks.',
    '<b>Run all tests:</b> python manage.py test  (optionally --verbosity 2).',
    '<b>Code quality checks:</b> python manage.py check  (system checks) and python -m compileall . for syntax.',
]:
    story += B(b)
story += H2('6.2 Recommended Test Matrix')
story.append(make_table(
    [('Module', 'Test Case', 'Expected Result')] +
    [
        ['accounts', 'Register student / teacher', 'User created with correct role; auto-login'],
        ['accounts', 'Login with wrong password', 'Form invalid; no session created'],
        ['accounts', 'Profile update', 'Fields persist; picture upload saved'],
        ['attendance', 'Teacher creates class', 'Class saved with teacher FK'],
        ['attendance', 'Student in wrong class scans QR', '403 / error message (not enrolled)'],
        ['attendance', 'Duplicate scan same session', 'Only one record (unique_together)'],
        ['attendance', 'Expired session scan', 'Session rejected (is_active False)'],
        ['attendance', 'Export Excel / PDF', 'HTTP 200, correct content-type'],
        ['timetable', 'Planner auto-suggestion', 'Tasks limited to enrolled subjects'],
        ['timetable', 'Complete a task', 'completed_tasks updated'],
        ['analytics', 'Student with &lt;75% flagged', 'Status = danger in subject_stats'],
        ['api', 'POST /api/mark-attendance/ valid session', 'success True, record created'],
        ['api', 'GET /api/student/attendance/ as teacher', '403 Forbidden'],
    ],
    [26 * mm, 76 * mm, 88 * mm]
))
story += H2('6.3 Sample Test Snippets')
story += H3('Model test - unique attendance')
story += CODE([
    'from django.test import TestCase',
    'class AttendanceTests(TestCase):',
    '    def test_unique_record_per_student(self):',
    '        # create student, class, session ...',
    '        AttendanceRecord.objects.create(session=s, student=st)',
    '        with self.assertRaises(Exception):',
    '            AttendanceRecord.objects.create(session=s, student=st)',
])
story += H3('View test - role guard')
story += CODE([
    'from django.test import TestCase',
    'from django.urls import reverse',
    'class GuardTests(TestCase):',
    '    def test_student_cannot_generate_qr(self):',
    '        self.client.login(username=\'student1\', password=\'student123\')',
    '        r = self.client.get(reverse(\'class_list\'))',
    '        self.assertEqual(r.status_code, 200)',
])
story += H3('API test with APIClient')
story += CODE([
    'from rest_framework.test import APIClient',
    'client = APIClient()',
    'client.login(username=\'student1\', password=\'student123\')',
    'r = client.post(\'/api/mark-attendance/\', {\'session_id\': qr_json}, format=\'json\')',
    'self.assertEqual(r.status_code, 200)',
])
story += H2('6.4 QA Checklist (before demo)')
for b in [
    'Register both roles and log in / out.',
    'Teacher: create class, generate QR, watch countdown, close session, export Excel &amp; PDF.',
    'Student: scan via camera, upload image, manual paste; attempt double scan (must fail).',
    'Expired session: wait for expiry or set short duration; scanning must be rejected.',
    'Timetable shows today; free periods detected; planner fills tasks for enrolled subjects.',
    'Analytics: charts render (Chart.js CDN), warning flags correct at 75% / 60% thresholds.',
    'Responsive layout at 1280px, 768px, 375px widths; sidebar collapse on mobile.',
    'Dark/light theme toggle persists after refresh.',
]:
    story += B(b)

# =====================================================================
# SECTION 7 - DEPLOYMENT & GIT  (Member 5)
# =====================================================================
story += section_cover('7', 'Deployment, Git &amp; GitHub', 'Member 5 - DevOps Engineer',
                       colors.HexColor('#FF6B9A'), 'Version control workflow, GitHub usage, Vercel '
                                                  'serverless deployment, and environment configuration.')
story += H2('7.1 Git Workflow')
story.append(make_table(
    [('Step', 'Command', 'Notes')] +
    [
        ['Clone repo', 'git clone &lt;repo-url&gt;', 'Initial pull'],
        ['Branch', 'git checkout -b feature/module', 'Member works on own branch'],
        ['Stage', 'git add .', 'Review with git status first'],
        ['Commit', 'git commit -m "type(scope): message"', 'e.g. feat(attendance): add qr export'],
        ['Pull main', 'git pull origin main', 'Keep in sync (rebase if needed)'],
        ['Push', 'git push origin feature/module', 'Upload branch'],
        ['PR', 'Open Pull Request on GitHub', 'Team Leader reviews & merges'],
        ['Merge', 'git checkout main && git merge feature/module', 'Only after review passes'],
    ],
    [20 * mm, 64 * mm, 106 * mm]
))
story += H2('7.2 Commit Conventions')
story.append(make_table(
    [('Type', 'When', 'Example')] +
    [
        ['feat', 'New feature', 'feat(analytics): add low-attendance warnings'],
        ['fix', 'Bug fix', 'fix(attendance): reject expired sessions'],
        ['refactor', 'No behaviour change', 'refactor(forms): simplify class form'],
        ['docs', 'Documentation', 'docs: update README'],
        ['test', 'Tests', 'test(api): cover mark-attendance endpoint'],
        ['chore', 'Tooling / deps', 'chore: add openpyxl dependency'],
    ],
    [24 * mm, 44 * mm, 122 * mm]
))
story += H2('7.3 GitHub Repository Hygiene')
for b in [
    'Keep <b>.gitignore</b> active: db.sqlite3, media/, staticfiles/, __pycache__/, .env, venv.',
    'Never commit secrets - store them as GitHub repository <b>Secrets</b> or Vercel <b>Environment Variables</b>.',
    'Main branch is protected in spirit: only the Team Leader merges PRs after review.',
    'README.md documents setup + default credentials for judges/demo machines.',
]:
    story += B(b)
story += H2('7.4 Vercel Deployment')
story += P('The project deploys as a Python serverless app on Vercel. The build pipeline runs migrations, '
           'seeds demo data and collects static files automatically (see vercel.json).')
story += CODE([
    '{',
    '  "version": 2,',
    '  "buildCommand": "python manage.py migrate --noinput &&',
    '                   python manage.py seed_data &&',
    '                   python manage.py collectstatic --noinput"',
    '}',
])
story += H2('7.5 Required Environment Variables')
story.append(make_table(
    [('Variable', 'Purpose', 'Example')] +
    [
        ['DJANGO_SECRET_KEY', 'Django signing secret', '<random long string>'],
        ['DJANGO_DEBUG', 'Debug mode', 'False'],
        ['DJANGO_ALLOWED_HOSTS', 'Allowed hostnames', '*.vercel.app, your-domain.com'],
        ['DJANGO_CSRF_TRUSTED_ORIGINS', 'CSRF-safe origins', 'https://*.vercel.app'],
        ['DATABASE_URL / POSTGRES_URL', 'Production Postgres DSN', 'postgres://user:pass@host/db'],
    ],
    [50 * mm, 62 * mm, 78 * mm]
))
story += H2('7.6 Local Development Commands')
story += CODE([
    '# 1. Install dependencies',
    'python -m venv .venv && .venv\\Scripts\\activate    (Windows)',
    'pip install -r requirements.txt',
    '',
    '# 2. Database',
    'python manage.py makemigrations',
    'python manage.py migrate',
    'python manage.py seed_data',
    '',
    '# 3. Run',
    'python manage.py runserver',
    '',
    '# 4. Verify',
    'python manage.py check',
    'python manage.py test',
])

# =====================================================================
# SECTION 8 - DEMO DATA & RUN GUIDE  (Leader)
# =====================================================================
story += section_cover('8', 'Demo Data, Credentials &amp; Run Guide', 'Team Leader - must know everything',
                       DARK, 'Ready-made accounts and the exact steps to run a smooth demo.')
story += H2('8.1 Seed Credentials')
story.append(make_table(
    [('Role', 'Username', 'Password', 'Count')] +
    [
        ['Admin', 'admin', 'admin123', '1'],
        ['Teachers', 'teacher1, teacher2, teacher3', 'teacher123', '3'],
        ['Students', 'student1 ... student8', 'student123', '8'],
    ],
    [30 * mm, 58 * mm, 44 * mm, 58 * mm]
))
story += H2('8.2 Demo Script (5 minutes)')
for step, txt in [
    ('1', 'Open the deployed URL; show the login page (Team Leader intro).'),
    ('2', 'Log in as teacher1 -> Dashboard -> My Classes -> open a class -> Generate QR (short duration, e.g. 5 min).'),
    ('3', 'Open the student mark-attendance page in another tab/device; scan the QR with camera (or upload the saved PNG). Success overlay appears.'),
    ('4', 'Show session detail: live count, absent list, then export Excel and PDF.'),
    ('5', 'Student logs in -> Dashboard shows attendance % per subject, then Analytics for charts.'),
    ('6', 'Show Timetable (today + free periods) and Daily Planner with auto-suggested tasks.'),
    ('7', 'Teacher Analytics: 14-day trend + low-attendance warning list.'),
    ('8', 'Close with the roadmap (future work).'),
]:
    story += B(f'<b>Step {step}:</b> {txt}')
story += H2('8.3 Troubleshooting')
story.append(make_table(
    [('Symptom', 'Likely Cause', 'Fix')] +
    [
        ['QR image not saved', 'media/ missing', 'mkdir media or run collectstatic'],
        ['Charts not rendering', 'Chart.js CDN blocked offline', 'Check internet or vendor the library'],
        ['Camera permission denied', 'Insecure context', 'Use https:// or localhost'],
        ['Scan says \'not enrolled\'', 'Student not in Class.students', 'Add student via admin / class form'],
        ['Vercel build fails', 'Env vars missing', 'Set DATABASE_URL + SECRET_KEY in Vercel'],
    ],
    [46 * mm, 58 * mm, 86 * mm]
))

# =====================================================================
# SECTION 9 - CONCLUSION
# =====================================================================
story += section_cover('9', 'Conclusion &amp; Future Roadmap', 'Team Leader - must know everything',
                       ACCENT, 'Final summary and next steps after the internal round.')
story += H2('9.1 What Was Delivered')
for b in [
    'A complete, role-aware attendance + free-period optimization platform in Django.',
    'QR-based attendance with expiry, duplicate protection and instant feedback.',
    'Automated daily planner that converts empty periods into guided study time.',
    'Teacher and student analytics with 75% rule warnings and Excel/PDF exports.',
    'A 6-member team with clearly separated, documented module ownership.',
]:
    story += B(b)
story += H2('9.2 Future Roadmap')
story.append(make_table(
    [('Idea', 'Description', 'Owner')] +
    [
        ['Geo-fencing / geolocation', 'Restrict scanning to classroom GPS radius (fields already exist)', 'Backend'],
        ['AI task suggestions', 'Rank TaskSuggestions by student performance &amp; subject weakness', 'Backend + Frontend'],
        ['Live attendance wall', 'Projector view with real-time present/absent grid', 'Frontend'],
        ['Push notifications', 'Remind students before free periods with suggested tasks', 'Backend + DevOps'],
        ['Bulk CSV import', 'Import students/classes from college ERP exports', 'Database'],
        ['E2E browser tests', 'Selenium/Playwright flows covering the demo script', 'Testing'],
        ['CI/CD pipeline', 'Run tests + checks automatically on every PR via GitHub Actions', 'DevOps'],
    ],
    [40 * mm, 78 * mm, 72 * mm]
))
story += H2('9.3 Closing Note')
story += P(
    'Every member knows their module inside out and the Team Leader understands how every module '
    'connects. Use this handbook for preparation, the demo script for the live round, and keep the '
    'code on GitHub as the single source of truth. Good luck, Team!')

# ---------------- Build ----------------
doc = SimpleDocTemplate(
    OUTPUT, pagesize=A4,
    rightMargin=15 * mm, leftMargin=15 * mm, topMargin=15 * mm, bottomMargin=15 * mm,
    title='SmartCurriculum - SIH 2026 Team Report',
    author='Team SmartCurriculum (6 members)',
)

def on_page(canvas, doc_):
    canvas.saveState()
    canvas.setFillColor(DARK)
    canvas.rect(0, A4[1] - 8 * mm, A4[0], 8 * mm, stroke=0, fill=1)
    canvas.setFillColor(colors.white)
    canvas.setFont('Helvetica-Bold', 8)
    canvas.drawString(15 * mm, A4[1] - 5.2 * mm, 'SmartCurriculum | SIH 2026 | Internal Round')
    canvas.setFont('Helvetica', 8)
    canvas.drawRightString(A4[0] - 15 * mm, A4[1] - 5.2 * mm, f'Page {canvas.getPageNumber()}')
    canvas.setFillColor(colors.HexColor('#CCCCDD'))
    canvas.setFont('Helvetica', 7.5)
    canvas.drawString(15 * mm, 8 * mm, 'Team Leader: full system  |  M1: SQL  |  M2: Django  |  M3: Frontend  |  M4: Testing  |  M5: DevOps')
    canvas.restoreState()

doc.build(story, onFirstPage=draw_cover, onLaterPages=on_page)
print(f'PDF generated: {OUTPUT}')

