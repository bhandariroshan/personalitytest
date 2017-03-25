from allauth.socialaccount.models import SocialToken
import facebook
import json
import requests
from action.models import UserLikes
# from mainapp.models import FacebookPost


def get_myfacebook_likes(myfacebook_graph, user):
    myfacebook_likes = []
    myfacebook_likes_info = myfacebook_graph.get_connections("me", "likes")

    while myfacebook_likes_info['data']:
        for like in myfacebook_likes_info['data']:
            myfacebook_likes.append(like)

            user_like  = UserLikes.objects.get_or_create(user=user)
            user_like.like = like
            user_like.save()

        if 'next' in myfacebook_likes_info['paging'].keys():
            myfacebook_likes_info = requests.get(myfacebook_likes_info['paging']['next']).json()
        else:
            break

    return myfacebook_likes
