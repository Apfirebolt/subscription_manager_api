from django.tasks import task
from django_scheduled_tasks import cron_task 

@cron_task(cron_schedule="* * * * *") # Runs at 9:00 AM every day
@task
def send_daily_reports():
    # Your background logic here
    print('This would be triggered every minute')