from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger

from mainapp.pull_likes import get_myfacebook_likes
from action.models import UserData

logger = get_task_logger(__name__)


# A periodic task that will run every minute (the symbol "*" means every)
@periodic_task(run_every=(crontab(hour="*", minute=0, day_of_week="*")))
def pull_user_likes():
    logger.info("Start task of pulling user likes")
    user_datas = UserData.objects.filter(likes__isnull=True)
    for each_user in user_datas:
        tokens = SocialToken.objects.filter(
            account__user=each_user.user,
            account__provider='facebook'
        )

        if tokens and not user_data:
            myfbgraph = facebook.GraphAPI(tokens[0].token)
            my_likes = get_myfacebook_likes(myfbgraph)
            each_user.likes = my_likes
            each_user.save()

    logger.info("Task finished: result = %i" % bool(result))
