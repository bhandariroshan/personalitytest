from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger

from mainapp.update_posts import update_posts

logger = get_task_logger(__name__)


# A periodic task that will run every minute (the symbol "*" means every)
@periodic_task(run_every=(crontab(hour="*", minute=0, day_of_week="*")))
def hourly_page_post_update():
    logger.info("Start task of updating page posts")
    result = update_posts()
    logger.info("Task finished: result = %i" % bool(result))
