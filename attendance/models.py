from django.db import models
from django.utils import timezone
import uuid


class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=100)
    credits = models.IntegerField(default=3)

    def __str__(self):
        return f"{self.code} - {self.name}"


class Class(models.Model):
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    year = models.IntegerField()
    section = models.CharField(max_length=10)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(
        'accounts.CustomUser',
        on_delete=models.CASCADE,
        related_name='teaching_classes',
        limit_choices_to={'role': 'teacher'}
    )
    students = models.ManyToManyField(
        'accounts.CustomUser',
        related_name='enrolled_classes',
        blank=True,
        limit_choices_to={'role': 'student'}
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject.code} ({self.teacher.get_full_name()})"

    class Meta:
        verbose_name_plural = "Classes"


class AttendanceSession(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('closed', 'Closed'),
    ]
    session_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='sessions')
    teacher = models.ForeignKey(
        'accounts.CustomUser',
        on_delete=models.CASCADE,
        related_name='created_sessions'
    )
    date = models.DateField(default=timezone.now)
    start_time = models.TimeField(default=timezone.now)
    end_time = models.TimeField(null=True, blank=True)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)
    qr_data = models.CharField(max_length=500, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    expires_at = models.DateTimeField(null=True, blank=True)
    location = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Session: {self.class_obj} - {self.date}"

    def is_active(self):
        if self.status == 'active':
            if self.expires_at and timezone.now() > self.expires_at:
                self.status = 'expired'
                self.save()
                return False
            return True
        return False

    class Meta:
        ordering = ['-created_at']


class AttendanceRecord(models.Model):
    STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
    ]
    session = models.ForeignKey(AttendanceSession, on_delete=models.CASCADE, related_name='records')
    student = models.ForeignKey(
        'accounts.CustomUser',
        on_delete=models.CASCADE,
        related_name='attendance_records'
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='present')
    marked_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    device_info = models.CharField(max_length=500, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    class Meta:
        unique_together = ['session', 'student']
        ordering = ['-marked_at']

    def __str__(self):
        return f"{self.student} - {self.session} - {self.status}"
