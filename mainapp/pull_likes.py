from allauth.socialaccount.models import SocialToken
import facebook
import json
import requests
from action.models import UserLikes, UserData
# from mainapp.models import FacebookPost


def get_myfacebook_likes(myfacebook_graph, user):
    myfacebook_likes = []
    myfacebook_likes_info = myfacebook_graph.get_connections("me", "likes")

    while myfacebook_likes_info['data']:
        for like in myfacebook_likes_info['data']:
            myfacebook_likes.append(like)

            user_like  = UserLikes.objects.get_or_create(user=user, like=like)
            user_like[0].like = like
            user_like[0].save()

        

        if 'next' in myfacebook_likes_info['paging'].keys():
            myfacebook_likes_info = requests.get(myfacebook_likes_info['paging']['next']).json()
        else:
            break

    user_data = UserData.objects.filter(user=user)
    user_data[0].likes_pulled = True
    user_data[0].save()

    return myfacebook_likes
