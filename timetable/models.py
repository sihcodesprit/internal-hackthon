from django.db import models
from django.utils import timezone


class TimeSlot(models.Model):
    DAY_CHOICES = [
        ('MON', 'Monday'),
        ('TUE', 'Tuesday'),
        ('WED', 'Wednesday'),
        ('THU', 'Thursday'),
        ('FRI', 'Friday'),
        ('SAT', 'Saturday'),
    ]
    SLOT_TYPE = [
        ('class', 'Class'),
        ('free', 'Free Period'),
        ('lunch', 'Lunch Break'),
        ('lab', 'Lab'),
    ]
    class_obj = models.ForeignKey(
        'attendance.Class',
        on_delete=models.CASCADE,
        related_name='time_slots',
        null=True, blank=True
    )
    day = models.CharField(max_length=3, choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    slot_type = models.CharField(max_length=20, choices=SLOT_TYPE, default='class')
    room_number = models.CharField(max_length=50, blank=True)
    department = models.CharField(max_length=100, blank=True)
    year = models.IntegerField(null=True, blank=True)
    section = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return f"{self.day} {self.start_time}-{self.end_time}: {self.slot_type}"

    class Meta:
        ordering = ['day', 'start_time']


class TaskSuggestion(models.Model):
    CATEGORY_CHOICES = [
        ('study', 'Self Study'),
        ('revision', 'Revision'),
        ('assignment', 'Assignment'),
        ('project', 'Project Work'),
        ('reading', 'Reading'),
        ('practice', 'Practice Problems'),
        ('research', 'Research'),
    ]
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    subject = models.ForeignKey('attendance.Subject', on_delete=models.CASCADE, null=True, blank=True)
    duration_minutes = models.IntegerField(default=30)
    priority = models.IntegerField(default=1)  # 1=low, 2=medium, 3=high
    resources_link = models.URLField(blank=True)

    def __str__(self):
        return self.title


class DailyPlanner(models.Model):
    student = models.ForeignKey(
        'accounts.CustomUser',
        on_delete=models.CASCADE,
        related_name='daily_planners'
    )
    date = models.DateField(default=timezone.now)
    tasks = models.ManyToManyField(TaskSuggestion, blank=True)
    custom_notes = models.TextField(blank=True)
    completed_tasks = models.ManyToManyField(
        TaskSuggestion,
        related_name='completed_by',
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['student', 'date']

    def __str__(self):
        return f"Planner - {self.student} - {self.date}"
