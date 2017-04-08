from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger

from .pull_likes import get_myfacebook_likes
from action.models import UserData, UserLikes
import requests
import json
import facebook
from allauth.socialaccount.models import SocialToken

logger = get_task_logger(__name__)


# A periodic task that will run every minute (the symbol "*" means every)
@periodic_task(run_every=(crontab(hour="*", minute="*", day_of_week="*")))
def pull_user_likes():
    logger.info("Start task of pulling user likes")
    user_datas = UserData.objects.filter(likes_pulled=False)
    print(user_datas)

    for each_userdata in user_datas:
        tokens = SocialToken.objects.filter(
            account__user=each_userdata.user,
            account__provider='facebook'
        )
        print(tokens)
        myfbgraph = facebook.GraphAPI(tokens[0].token)
        myfacebook_likes_info = myfbgraph.get_connections("me", "likes")
        print(myfacebook_likes_info['data'])
        myfacebook_likes = []
        while myfacebook_likes_info['data']:
            for like in myfacebook_likes_info['data']:
                myfacebook_likes.append(like)
                print(like)

                user_like  = UserLikes.objects.get_or_create(user=each_userdata.user, like=like)
                user_like[0].like = like
                user_like[0].save()

            if 'next' in myfacebook_likes_info['paging'].keys():
                myfacebook_likes_info = requests.get(myfacebook_likes_info['paging']['next']).json()
            else:
                break
        
        each_userdata.likes_pulled = True
        each_userdata.save()

    logger.info("Task finished: result = %i" % bool(result))
