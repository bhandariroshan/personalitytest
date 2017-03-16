import json
from django.views.generic import View
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin

from allauth.socialaccount.models import SocialToken, SocialApp
from .models import FacebookPost


class DataPreview(LoginRequiredMixin, View):
    """Module for previewing data from facebook."""
    template_name = 'preview.html'

    def get_context_data(self, **kwargs):
        context = {}
        tokens = SocialToken.objects.filter(
            account__user=self.request.user,
            account__provider='facebook'
        )
        if tokens:
            context['token'] = tokens[0].token

        fb_app = get_object_or_404(SocialApp, id=1)
        context['app_id'] = fb_app.client_id
        return context

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data())


class GetPagePostsAPI(APIView):
    """Simple API to accept the POST data from javascript"""

    def get(self, request, *args, **kwargs):
        try:
            post = FacebookPost.objects.get(page_id=request.GET.get('page_id'))
            data = json.loads(post.most_liked_post)
        except:
            data = {"status": "Error"}
        return Response(data)

    def post(self, request, *args, **kwargs):
        data = dict(request.data)

        # sort posts based on number of likes
        posts = sorted(
            data.get('posts'), key=lambda k: k['total_likes'],
            reverse=True
        )

        # # Save the data to database
        post_obj, created = FacebookPost.objects.get_or_create(
            page_id=data['page_info']['id']
        )
        post_obj.posts = json.dumps(posts)
        post_obj.page_info = json.dumps(data.get('page_info'))
        post_obj.most_liked_post = json.dumps(posts[0])
        post_obj.save()

        # return second most liked post
        # print(posts)
        return Response(posts[1])
