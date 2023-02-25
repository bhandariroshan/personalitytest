from celery.schedules import crontab
from celery import Celery

from celery.utils.log import get_task_logger

from .pull_likes import get_myfacebook_likes
from action.models import UserData, UserLikes, PageSettings, PageConversation
import requests
import json
import facebook
from allauth.socialaccount.models import SocialToken

logger = get_task_logger(__name__)
app = Celery()

# A periodic task that will run every minute (the symbol "*" means every)
@app.periodic_task(run_every=(crontab(hour="*", minute="*", day_of_week="*")))
def pull_user_likes():
    logger.info("Start task of pulling user likes")
    user_datas = UserData.objects.filter(likes_pulled=False)

    for each_userdata in user_datas:
        tokens = SocialToken.objects.filter(
            account__user=each_userdata.user,
            account__provider='facebook'
        )
        myfbgraph = facebook.GraphAPI(tokens[0].token)
        myfacebook_likes_info = myfbgraph.get_connections("me", "likes")
        print("Likes Pull CALLED::",myfacebook_likes_info['data'])
        myfacebook_likes = []
        while myfacebook_likes_info['data']:
            for like in myfacebook_likes_info['data']:
                myfacebook_likes.append(like)

                user_like  = UserLikes.objects.get_or_create(user=each_userdata.user, like=like)
                user_like[0].like = like
                user_like[0].save()

            if 'next' in myfacebook_likes_info['paging'].keys():
                myfacebook_likes_info = requests.get(myfacebook_likes_info['paging']['next']).json()
            else:
                break
        
        print("completed Pulling, Pulled: " + str(len(myfacebook_likes)) + " Likes")
        each_userdata.likes_pulled = True
        each_userdata.save()


# A periodic task that will run every minute (the symbol "*" means every)
@app.periodic_task(run_every=(crontab(hour="*", minute="*", day_of_week="*")))
def pull_page_conversations():
    logger.info("Start task of pulling page conversations")
    user_datas = UserData.objects.filter(likes_pulled=False)
    tokens = PageSettings.objects.filter()

    # Retrive tasks
    # a. Page acccess token with permission to read messages and reply conversations and save it to model Page Settings
    # b. Page ID from where app will send the message

    # Steps for Jokes Delivery
    # 1. Retrieve page access token from https://developers.facebook.com/tools/explorer/666615676843865?method=GET&path=667782319960906%2Fconversations%20&version=v2.9
    # 2. Read all the conversations
    # 3. Register all conversations in database, 
    # 4. If Jokes not delivered, deliver joke

    # Read all conversations
    if tokens:
        base_url="https://graph.facebook.com/v2.9/" + tokens[0].pageid + "/conversations?"
        params="access_token=" + tokens[0].access_token
        access_token = tokens[0].access_token

    
    # get all page conversations
    conversations = requests.get(base_url+params).json()
    print('-------------------------------------------')
    print(conversations)
    print('-------------------------------------------')
    print(access_token)
    conversations =  conversations['data']

    for each_conversation in conversations:
        pc = PageConversation.objects.get_or_create(conversation=each_conversation)

        # Get a Joke and Send a Joke reply 
        # Get Conversation ID, Send Message
        joke = "Hi!! This is a Joke Sample. Please smile and laugh."
        payload = {
                "message": joke,
                "access_token":access_token
        }

        try:
            response = requests.post(
                "https://graph.facebook.com/v2.9/" + str(each_conversation['id']) + "/messages", 
                 data=json.dumps(payload),
                 headers = {"Content-Type": "application/json"}
            )
            print("Joke Sent")
            pc[0].conversation_replied = True
            pc[0].reply_message = joke

        except:
            pass

        pc[0].save()

    print("Jokes Send Complete!!")
