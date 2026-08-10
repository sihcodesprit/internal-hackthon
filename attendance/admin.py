from django.contrib import admin
from .models import Subject, Class, AttendanceSession, AttendanceRecord


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'department', 'credits']
    search_fields = ['name', 'code']
    list_filter = ['department']


@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ['name', 'subject', 'teacher', 'department', 'year', 'section']
    list_filter = ['department', 'year', 'section']
    search_fields = ['name', 'teacher__username']
    filter_horizontal = ['students']


@admin.register(AttendanceSession)
class AttendanceSessionAdmin(admin.ModelAdmin):
    list_display = ['session_id', 'class_obj', 'teacher', 'date', 'status', 'created_at']
    list_filter = ['status', 'date']
    search_fields = ['class_obj__name', 'teacher__username']
    readonly_fields = ['session_id', 'created_at']


@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ['student', 'session', 'status', 'marked_at']
    list_filter = ['status', 'marked_at']
    search_fields = ['student__username', 'session__class_obj__name']
