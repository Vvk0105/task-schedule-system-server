from django.core.management.base import BaseCommand
from scheduler.models import Task, TaskExecutionHistory
from scheduler.utils import get_next_run_time
from django.utils import timezone
import time
import random


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        while True:
            now = timezone.now()

            tasks = Task.objects.filter(is_active=True, is_paused=False, next_run_at__lte=now)

            for task in tasks:
                #  depandancy check 
                if task.depends_on:
                    parent = task.depends_on
                    if parent.last_status != "success":
                        TaskExecutionHistory.objects.create(
                            task=task,
                            status="skipped",
                            log=f"Skipped because parent task '{parent.name}' did not succeed."
                        )
                        continue
                
                # testing
                should_fail = random.choice([True, False]) 

                try:
                    if should_fail:
                        raise Exception("Simulated task failure!")

                    TaskExecutionHistory.objects.create(
                        task=task,
                        status="success",
                        log="Task executed successfully"
                    )

                    task.last_status = "success"
                    task.retry_count = 0
                    task.next_run_at = get_next_run_time(task.cron_expression)

                except Exception as e:
                    TaskExecutionHistory.objects.create(
                        task=task,
                        status="failed",
                        log=str(e)
                    )

                    task.last_status = "failed"

                    delay_minutes = 2 ** task.retry_count
                    task.retry_count += 1

                    task.next_run_at = now + timezone.timedelta(minutes=delay_minutes)

                task.save()

            time.sleep(10)
