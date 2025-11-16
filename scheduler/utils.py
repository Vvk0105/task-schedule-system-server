from croniter import croniter
from django.utils import timezone
from datetime import datetime

def get_next_run_time(cron_expression):
    now = timezone.localtime()
    cron = croniter(cron_expression, now)
    return cron.get_next(datetime)
