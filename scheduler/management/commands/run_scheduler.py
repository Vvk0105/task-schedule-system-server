from django.core.management.base import BaseCommand
from scheduler.models import Task, TaskExecutionHistory
from scheduler.utils import get_next_run_time
from django.utils import timezone
import time

class Command(BaseCommand):
    def handle(self, *args, **options):
        while True:
            now = timezone.now()

            tasks = Task.objects.filter(is_active=True, is_paused=False, next_run_at__lte=now)

            for task in tasks:
                TaskExecutionHistory.objects.create(
                    task,
                    status = 'success',
                    log = 'Task executed successfully'
                )
                task.last_status = "success"
                task.retry_count = 0
                task.next_run_at = get_next_run_time(task.cron_expression)
                task.save()

            time.sleep(10)