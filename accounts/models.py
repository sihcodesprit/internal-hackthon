from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    phone = models.CharField(max_length=15, blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    department = models.CharField(max_length=100, blank=True)
    roll_number = models.CharField(max_length=20, blank=True)  # for students
    employee_id = models.CharField(max_length=20, blank=True)  # for teachers
    year_of_study = models.IntegerField(null=True, blank=True)  # for students
    section = models.CharField(max_length=10, blank=True)

    def is_teacher(self):
        return self.role == 'teacher'

    def is_student(self):
        return self.role == 'student'

    def is_admin_user(self):
        return self.role == 'admin'

    def __str__(self):
        return f"{self.get_full_name()} ({self.role})"
