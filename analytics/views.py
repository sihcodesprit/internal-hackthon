from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Avg, Q
from django.utils import timezone
from datetime import timedelta
from attendance.models import Class, AttendanceSession, AttendanceRecord
from accounts.models import CustomUser


@login_required
def analytics_dashboard(request):
    if request.user.is_teacher():
        return teacher_analytics(request)
    else:
        return student_analytics(request)


def teacher_analytics(request):
    teacher = request.user
    classes = Class.objects.filter(teacher=teacher)
    today = timezone.now().date()
    last_30_days = today - timedelta(days=30)

    # Daily attendance trend (last 14 days)
    daily_trend = []
    for i in range(13, -1, -1):
        day = today - timedelta(days=i)
        sessions = AttendanceSession.objects.filter(teacher=teacher, date=day)
        total_present = AttendanceRecord.objects.filter(
            session__in=sessions, status='present'
        ).count()
        total_students = sum(s.class_obj.students.count() for s in sessions)
        pct = round((total_present / total_students * 100) if total_students > 0 else 0, 1)
        daily_trend.append({'date': str(day), 'percentage': pct, 'count': total_present})

    # Class-wise summary
    class_summary = []
    for cls in classes:
        total_sessions = AttendanceSession.objects.filter(class_obj=cls).count()
        total_students = cls.students.count()
        total_possible = total_sessions * total_students
        total_present = AttendanceRecord.objects.filter(
            session__class_obj=cls, status='present'
        ).count()
        pct = round((total_present / total_possible * 100) if total_possible > 0 else 0, 1)
        class_summary.append({
            'class': cls,
            'sessions': total_sessions,
            'students': total_students,
            'avg_attendance': pct
        })

    # Low attendance students (below 75%)
    low_attendance = []
    for cls in classes:
        for student in cls.students.all():
            total = AttendanceSession.objects.filter(class_obj=cls).count()
            present = AttendanceRecord.objects.filter(
                student=student, session__class_obj=cls, status='present'
            ).count()
            pct = round((present / total * 100) if total > 0 else 0, 1)
            if pct < 75 and total > 0:
                low_attendance.append({'student': student, 'class': cls, 'percentage': pct})

    context = {
        'classes': classes,
        'class_summary': class_summary,
        'daily_trend': daily_trend,
        'low_attendance': low_attendance[:10],
        'total_sessions_today': AttendanceSession.objects.filter(teacher=teacher, date=today).count(),
        'total_classes': classes.count(),
        'total_students': CustomUser.objects.filter(enrolled_classes__teacher=teacher).distinct().count(),
    }
    return render(request, 'analytics/teacher_analytics.html', context)


def student_analytics(request):
    student = request.user
    enrolled_classes = student.enrolled_classes.select_related('subject', 'teacher')
    today = timezone.now().date()

    # Per-subject attendance
    subject_stats = []
    for cls in enrolled_classes:
        total = AttendanceSession.objects.filter(class_obj=cls).count()
        present = AttendanceRecord.objects.filter(
            student=student, session__class_obj=cls, status='present'
        ).count()
        pct = round((present / total * 100) if total > 0 else 0, 1)
        needed_for_75 = max(0, int(0.75 * total) - present)
        subject_stats.append({
            'class': cls,
            'total': total,
            'present': present,
            'absent': total - present,
            'percentage': pct,
            'needed_for_75': needed_for_75,
            'status': 'safe' if pct >= 75 else ('warning' if pct >= 60 else 'danger')
        })

    # Monthly trend
    monthly_trend = []
    for i in range(29, -1, -1):
        day = today - timedelta(days=i)
        records = AttendanceRecord.objects.filter(student=student, session__date=day)
        present = records.filter(status='present').count()
        total = records.count()
        monthly_trend.append({
            'date': str(day),
            'present': present,
            'total': total,
        })

    # Overall stats
    total_records = AttendanceRecord.objects.filter(student=student)
    overall_present = total_records.filter(status='present').count()
    overall_total = total_records.count()
    overall_pct = round((overall_present / overall_total * 100) if overall_total > 0 else 0, 1)

    context = {
        'subject_stats': subject_stats,
        'monthly_trend': monthly_trend,
        'overall_present': overall_present,
        'overall_total': overall_total,
        'overall_pct': overall_pct,
        'today': today,
    }
    return render(request, 'analytics/student_analytics.html', context)
