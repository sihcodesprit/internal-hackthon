from django.urls import path
from . import api_views

urlpatterns = [
    path('mark-attendance/', api_views.api_mark_attendance, name='api_mark_attendance'),
    path('session/<uuid:session_id>/status/', api_views.api_session_status, name='api_session_status'),
    path('student/attendance/', api_views.api_student_attendance, name='api_student_attendance'),
    path('student/active-sessions/', api_views.api_active_sessions, name='api_active_sessions'),
]
