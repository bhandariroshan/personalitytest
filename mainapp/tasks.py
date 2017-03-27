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

    for each_user in user_datas:
        print(each_user.user)

        tokens = SocialToken.objects.filter(
            account__user=each_user.user,
            account__provider='facebook'
        )

        print(tokens)
        
        myfbgraph = facebook.GraphAPI(tokens[0].token)
        print("1")
        myfacebook_likes_info = myfbgraph.get_connections("me", "likes")
        print("2")

        myfacebook_likes = []
        while myfacebook_likes_info['data']:
            print("3")
            for like in myfacebook_likes_info['data']:
                print("4")
                myfacebook_likes.append(like)

                user_like  = UserLikes.objects.get_or_create(user=each_user.user, like=like)
                user_like[0].like = like
                user_like[0].save()

            if 'next' in myfacebook_likes_info['paging'].keys():
                myfacebook_likes_info = requests.get(myfacebook_likes_info['paging']['next']).json()
            else:
                break

        print("CALLED")
        
        each_user.likes_pulled = True
        each_user.save()


        print("COMPLETE")

    logger.info("Task finished: result = %i" % bool(result))
