from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import TimeSlot, TaskSuggestion, DailyPlanner
import datetime


@login_required
def timetable_view(request):
    user = request.user
    if user.is_student():
        slots = TimeSlot.objects.filter(
            department=user.department,
            year=user.year_of_study,
            section=user.section
        ).select_related('class_obj__subject', 'class_obj__teacher').order_by('day', 'start_time')
    else:
        slots = TimeSlot.objects.filter(
            class_obj__teacher=user
        ).select_related('class_obj__subject').order_by('day', 'start_time')

    days = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT']
    day_labels = {'MON': 'Monday', 'TUE': 'Tuesday', 'WED': 'Wednesday',
                  'THU': 'Thursday', 'FRI': 'Friday', 'SAT': 'Saturday'}
    timetable = {day: [] for day in days}
    for slot in slots:
        timetable[slot.day].append(slot)

    today = timezone.now().date()
    today_day = today.strftime('%A')[:3].upper()
    today_slots = timetable.get(today_day, [])
    free_periods = [s for s in today_slots if s.slot_type == 'free']

    return render(request, 'timetable/timetable.html', {
        'timetable': timetable,
        'days': days,
        'day_labels': day_labels,
        'today': today,
        'today_day': today_day,
        'today_slots': today_slots,
        'free_periods': free_periods,
    })


@login_required
def daily_planner(request):
    if not request.user.is_student():
        messages.error(request, 'Daily planner is for students only.')
        return redirect('dashboard')

    today = timezone.now().date()
    today_day = today.strftime('%A')[:3].upper()

    # Get today's slots
    slots = TimeSlot.objects.filter(
        department=request.user.department,
        year=request.user.year_of_study,
        section=request.user.section,
        day=today_day
    ).select_related('class_obj__subject')

    free_slots = [s for s in slots if s.slot_type == 'free']

    # Get or create planner for today
    planner, created = DailyPlanner.objects.get_or_create(
        student=request.user, date=today
    )

    # Auto-suggest tasks for free periods
    if created or not planner.tasks.exists():
        # Get subjects from enrolled classes
        subjects = [cls.subject for cls in request.user.enrolled_classes.all()]
        suggestions = TaskSuggestion.objects.filter(
            subject__in=subjects
        ).order_by('-priority')[:len(free_slots) * 2 + 3] if subjects else TaskSuggestion.objects.order_by('-priority')[:5]
        planner.tasks.set(suggestions)

    if request.method == 'POST':
        completed_ids = request.POST.getlist('completed_tasks')
        notes = request.POST.get('notes', '')
        planner.completed_tasks.set(completed_ids)
        planner.custom_notes = notes
        planner.save()
        messages.success(request, 'Planner updated!')
        return redirect('daily_planner')

    tasks = planner.tasks.all()
    completed_tasks = planner.completed_tasks.all()

    return render(request, 'timetable/daily_planner.html', {
        'planner': planner,
        'tasks': tasks,
        'completed_tasks': completed_tasks,
        'free_slots': free_slots,
        'today': today,
        'today_slots': slots,
    })
