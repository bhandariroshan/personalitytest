from allauth.socialaccount.models import SocialToken
import facebook
import json

from mainapp.models import FacebookPost


def update_posts(page_id='209242849219109'):
    try:
        tokens = SocialToken.objects.all()
        access_token = tokens[0].token
    except:
        access_token = None
    if access_token:
        graph = facebook.GraphAPI(access_token=access_token, version='2.6')
        page_info = get_page_info(graph)
        page_posts = get_page_posts(graph)
        for post in page_posts:
            likes = get_post_likes(graph, str(post['id']))
            post['total_likes'] = likes
        sorted_posts = sorted(
            page_posts, key=lambda k: k['total_likes'],
            reverse=True
        )

        post_obj, created = FacebookPost.objects.get_or_create(
            page_id=page_id
        )
        post_obj.posts = json.dumps(sorted_posts)
        post_obj.page_info = json.dumps(page_info)
        post_obj.most_liked_post = json.dumps(sorted_posts[0])
        post_obj.save()
        return graph
    else:
        return


def get_page_info(graph, page_id='209242849219109'):
    page_info = graph.get_object(
        page_id +
        '/?fields=about,affiliation,bio,category,cover,'
        'engagement,fan_count,is_verified,link'
    )
    return page_info


def get_page_posts(graph, page_id='209242849219109'):
    posts = graph.get_object(
        page_id + '/posts/?fields=story,created_time,message,link')
    if posts.get('data'):
        return posts['data']


def get_post_likes(graph, post_id):
    post_likes = graph.get_object(
        post_id + '/likes/?summary=true'
    )
    if post_likes.get('summary'):
        return post_likes['summary']['total_count']
