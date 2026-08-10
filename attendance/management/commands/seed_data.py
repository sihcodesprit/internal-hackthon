"""
Management command to seed demo data for SmartCurriculum.
Run: python manage.py seed_data
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import time, timedelta, date
import random

User = get_user_model()


class Command(BaseCommand):
    help = 'Seed demo data for SmartCurriculum'

    def handle(self, *args, **options):
        self.stdout.write('[*] Seeding demo data...')

        # Import models here to avoid circular imports
        from attendance.models import Subject, Class, AttendanceSession, AttendanceRecord
        from timetable.models import TimeSlot, TaskSuggestion

        # ─────────────────────────────────────────────────────────
        # 1. Admin user
        # ─────────────────────────────────────────────────────────
        admin, _ = User.objects.get_or_create(username='admin', defaults={
            'email': 'admin@smartcurriculum.edu',
            'first_name': 'System',
            'last_name': 'Admin',
            'role': 'admin',
            'is_staff': True,
            'is_superuser': True,
        })
        admin.set_password('admin123')
        admin.save()
        self.stdout.write('  [+] Admin user created (admin / admin123)')

        # ─────────────────────────────────────────────────────────
        # 2. Teachers
        # ─────────────────────────────────────────────────────────
        teachers_data = [
            ('teacher1', 'Priya', 'Sharma', 'priya@college.edu', 'Computer Science', 'EMP001'),
            ('teacher2', 'Rajesh', 'Kumar', 'rajesh@college.edu', 'Computer Science', 'EMP002'),
            ('teacher3', 'Anita', 'Patel', 'anita@college.edu', 'Mathematics', 'EMP003'),
        ]
        teachers = []
        for uname, fname, lname, email, dept, emp_id in teachers_data:
            t, _ = User.objects.get_or_create(username=uname, defaults={
                'first_name': fname, 'last_name': lname,
                'email': email, 'department': dept,
                'employee_id': emp_id, 'role': 'teacher',
            })
            t.set_password('teacher123')
            t.save()
            teachers.append(t)
        self.stdout.write(f'  [+] {len(teachers)} teachers created (password: teacher123)')

        # ─────────────────────────────────────────────────────────
        # 3. Students
        # ─────────────────────────────────────────────────────────
        students_data = [
            ('student1', 'Arjun', 'Mehta', 'arjun@student.edu', 'CS21001', 3, 'A'),
            ('student2', 'Sneha', 'Nair', 'sneha@student.edu', 'CS21002', 3, 'A'),
            ('student3', 'Vikram', 'Singh', 'vikram@student.edu', 'CS21003', 3, 'A'),
            ('student4', 'Pooja', 'Reddy', 'pooja@student.edu', 'CS21004', 3, 'B'),
            ('student5', 'Rahul', 'Gupta', 'rahul@student.edu', 'CS21005', 3, 'A'),
            ('student6', 'Preethi', 'Rao', 'preethi@student.edu', 'CS21006', 3, 'B'),
            ('student7', 'Karthik', 'Iyer', 'karthik@student.edu', 'CS21007', 3, 'A'),
            ('student8', 'Divya', 'Menon', 'divya@student.edu', 'CS21008', 3, 'B'),
        ]
        students = []
        for uname, fname, lname, email, roll, year, sec in students_data:
            s, _ = User.objects.get_or_create(username=uname, defaults={
                'first_name': fname, 'last_name': lname,
                'email': email, 'roll_number': roll,
                'year_of_study': year, 'section': sec,
                'department': 'Computer Science', 'role': 'student',
            })
            s.set_password('student123')
            s.save()
            students.append(s)
        self.stdout.write(f'  [+] {len(students)} students created (password: student123)')

        # ─────────────────────────────────────────────────────────
        # 4. Subjects
        # ─────────────────────────────────────────────────────────
        subjects_data = [
            ('CS301', 'Data Structures & Algorithms', 'Computer Science', 4),
            ('CS302', 'Database Management Systems', 'Computer Science', 3),
            ('CS303', 'Operating Systems', 'Computer Science', 4),
            ('MA301', 'Discrete Mathematics', 'Mathematics', 3),
            ('CS304', 'Computer Networks', 'Computer Science', 3),
        ]
        subjects = []
        for code, name, dept, credits in subjects_data:
            subj, _ = Subject.objects.get_or_create(code=code, defaults={
                'name': name, 'department': dept, 'credits': credits
            })
            subjects.append(subj)
        self.stdout.write(f'  [+] {len(subjects)} subjects created')

        # ─────────────────────────────────────────────────────────
        # 5. Classes
        # ─────────────────────────────────────────────────────────
        classes_data = [
            ('CS-DSA-3A', 'Computer Science', 3, 'A', subjects[0], teachers[0]),
            ('CS-DBMS-3A', 'Computer Science', 3, 'A', subjects[1], teachers[0]),
            ('CS-OS-3B', 'Computer Science', 3, 'B', subjects[2], teachers[1]),
            ('MA-DM-3A', 'Computer Science', 3, 'A', subjects[3], teachers[2]),
        ]
        classes = []
        for name, dept, year, sec, subj, teacher in classes_data:
            cls, _ = Class.objects.get_or_create(name=name, defaults={
                'department': dept, 'year': year, 'section': sec,
                'subject': subj, 'teacher': teacher,
            })
            # Enroll students
            sec_students = [s for s in students if s.section == sec or name == 'MA-DM-3A']
            cls.students.set(sec_students)
            classes.append(cls)
        self.stdout.write(f'  [+] {len(classes)} classes created')

        # ─────────────────────────────────────────────────────────
        # 6. Attendance Sessions & Records (last 10 days)
        # ─────────────────────────────────────────────────────────
        today = timezone.now().date()
        session_count = 0
        record_count = 0
        for cls in classes[:3]:
            for i in range(10):
                sess_date = today - timedelta(days=i + 1)
                session = AttendanceSession.objects.filter(
                    class_obj=cls, date=sess_date
                ).first()
                if session is None:
                    session = AttendanceSession.objects.create(
                        class_obj=cls, date=sess_date,
                        teacher=cls.teacher,
                        start_time=time(9, 0),
                        status='closed',
                        expires_at=timezone.now() - timedelta(hours=1),
                    )
                    session_count += 1
                for student in cls.students.all():
                    # Randomize attendance (70-95% presence)
                    if random.random() < 0.82:
                        if not AttendanceRecord.objects.filter(
                            session=session, student=student
                        ).exists():
                            AttendanceRecord.objects.create(
                                session=session, student=student,
                                status='present'
                            )
                            record_count += 1
        self.stdout.write(f'  [+] {session_count} sessions, {record_count} attendance records')

        # ─────────────────────────────────────────────────────────
        # 7. Timetable Slots
        # ─────────────────────────────────────────────────────────
        days = ['MON', 'TUE', 'WED', 'THU', 'FRI']
        slot_templates = [
            (time(8, 0), time(9, 0), 'class', classes[0], '101'),    # DSA
            (time(9, 0), time(10, 0), 'class', classes[1], '102'),   # DBMS
            (time(10, 0), time(10, 30), 'free', None, ''),           # Free
            (time(10, 30), time(11, 30), 'class', classes[3], '201'), # Maths
            (time(11, 30), time(12, 30), 'class', None, ''),         # Free
            (time(12, 30), time(13, 30), 'lunch', None, ''),         # Lunch
            (time(13, 30), time(14, 30), 'class', classes[2], 'Lab1'), # OS
            (time(14, 30), time(15, 30), 'free', None, ''),          # Free
        ]
        for day in days:
            for start, end, stype, cls_obj, room in slot_templates:
                TimeSlot.objects.get_or_create(
                    day=day, start_time=start, end_time=end,
                    slot_type=stype, department='Computer Science',
                    year=3, section='A',
                    defaults={'class_obj': cls_obj, 'room_number': room}
                )
        self.stdout.write(f'  [+] Timetable slots created')

        # ─────────────────────────────────────────────────────────
        # 8. Task Suggestions
        # ─────────────────────────────────────────────────────────
        tasks_data = [
            ('Solve 10 LeetCode problems', 'Practice DSA problems - arrays and strings', 'practice', subjects[0], 60, 3),
            ('Review Database Normalization', 'Revise 1NF, 2NF, 3NF, BCNF concepts', 'revision', subjects[1], 45, 2),
            ('Read OS Chapter 5', 'Study process scheduling algorithms', 'reading', subjects[2], 30, 2),
            ('Complete Math Assignment', 'Solve graph theory exercises from textbook', 'assignment', subjects[3], 90, 3),
            ('Network Protocol Research', 'Study TCP/IP model and protocols', 'research', subjects[4], 45, 2),
            ('DSA Project Work', 'Work on binary search tree implementation', 'project', subjects[0], 120, 1),
            ('Self Study - DBMS', 'Practice SQL queries and joins', 'study', subjects[1], 60, 2),
            ('OS Revision Notes', 'Create revision notes for memory management', 'revision', subjects[2], 30, 1),
            ('Math Problem Practice', 'Solve discrete math problems', 'practice', subjects[3], 45, 2),
            ('Complete CN Lab Report', 'Document network simulation lab work', 'assignment', subjects[4], 60, 3),
        ]
        for title, desc, cat, subj, dur, pri in tasks_data:
            TaskSuggestion.objects.get_or_create(title=title, defaults={
                'description': desc, 'category': cat,
                'subject': subj, 'duration_minutes': dur, 'priority': pri
            })
        self.stdout.write(f'  [+] {len(tasks_data)} task suggestions created')

        self.stdout.write(self.style.SUCCESS('\nDemo data seeded successfully!'))
        self.stdout.write('\nCredentials:')
        self.stdout.write('  Admin:   admin / admin123')
        self.stdout.write('  Teachers: teacher1, teacher2, teacher3 / teacher123')
        self.stdout.write('  Students: student1 to student8 / student123')
        self.stdout.write('\nRun: python manage.py runserver')
