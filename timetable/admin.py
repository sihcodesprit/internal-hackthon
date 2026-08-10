from django.contrib import admin
from .models import TimeSlot, TaskSuggestion, DailyPlanner


@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ['day', 'start_time', 'end_time', 'slot_type', 'class_obj', 'room_number', 'department', 'year', 'section']
    list_filter = ['day', 'slot_type', 'department', 'year']
    ordering = ['day', 'start_time']


@admin.register(TaskSuggestion)
class TaskSuggestionAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'subject', 'duration_minutes', 'priority']
    list_filter = ['category', 'priority']
    search_fields = ['title', 'description']


@admin.register(DailyPlanner)
class DailyPlannerAdmin(admin.ModelAdmin):
    list_display = ['student', 'date', 'created_at']
    list_filter = ['date']
    search_fields = ['student__username']
