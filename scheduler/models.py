from django.db import models
from django.utils import timezone
# Create your models here.

class Task(models.Model):
    name = models.CharField(max_length=200)
    cron_expression = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_paused = models.BooleanField(default=False)
    next_run_at = models.DateTimeField(null=True, blank=True)
    retry_count = models.IntegerField(default=0)
    last_status = models.CharField(max_length=20, default="pending")
    depends_on = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.SET_NULL, related_name='dependent_tasks'
    )

    def __str__(self):
        return self.name

class TaskExecutionHistory(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20)
    log = models.TextField()

    def __str__(self):
        return f"{self.task.name} - {self.status}"
