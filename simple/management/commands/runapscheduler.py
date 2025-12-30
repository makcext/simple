import logging

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django.core.management.base import BaseCommand
from django_apscheduler import util
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_dramatiq.tasks import delete_old_tasks

from simple.processes.get_weather import get_weather_data

logger = logging.getLogger(__name__)


@util.close_old_connections
def delete_old_job_executions(max_age=1_209_600):
    """
    This job deletes APScheduler job execution entries older than `max_age` from the database.
    It helps to prevent the database from filling up with old historical records that are no
    longer useful.

    :param max_age: The maximum length of time to retain historical job execution records.
                    Defaults to 14 days.
    """
    DjangoJobExecution.objects.delete_old_job_executions(max_age)
    delete_old_tasks(max_age)


@util.close_old_connections
def fetch_weather_data():
    """
    Fetch weather data from OpenWeatherMap API and save to database.
    """
    logger.info("Starting weather data fetch job...")
    success, message = get_weather_data()

    if success:
        logger.info(f"Weather data fetch successful: {message}")
    else:
        logger.error(f"Weather data fetch failed: {message}")


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: 'delete_old_job_executions'.")

        scheduler.add_job(
            fetch_weather_data,
            trigger=CronTrigger(minute="*/5"),
            id="fetch_weather_data",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added periodic job (every 5 minutes): 'fetch_weather_data'.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
