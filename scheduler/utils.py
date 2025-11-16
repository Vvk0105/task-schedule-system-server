from croniter import croniter
from datetime import datetime

def get_next_run_time(cron_expression):
    now = datetime.now()
    cron = croniter(cron_expression, now)
    return cron.get_next(datetime)
