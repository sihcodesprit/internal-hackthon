from django.urls import path
from . import views

urlpatterns = [
    path('', views.timetable_view, name='timetable'),
    path('planner/', views.daily_planner, name='daily_planner'),
]
