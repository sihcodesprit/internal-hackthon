from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('classes/', views.class_list, name='class_list'),
    path('classes/create/', views.class_create, name='class_create'),
    path('classes/<int:pk>/', views.class_detail, name='class_detail'),
    path('classes/<int:class_id>/generate-qr/', views.generate_qr, name='generate_qr'),
    path('attendance/mark/', views.mark_attendance, name='mark_attendance'),
    path('attendance/history/', views.attendance_history, name='attendance_history'),
    path('attendance/session/<uuid:session_id>/', views.session_detail, name='session_detail'),
    path('attendance/session/<uuid:session_id>/close/', views.close_session, name='close_session'),
    path('attendance/session/<uuid:session_id>/export/excel/', views.export_attendance_excel, name='export_excel'),
    path('attendance/session/<uuid:session_id>/export/pdf/', views.export_attendance_pdf, name='export_pdf'),
]
