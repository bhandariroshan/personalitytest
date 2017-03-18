# -*- coding: utf-8 -*-
import json
from django.views.generic import View
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
import facebook
from allauth.socialaccount.models import SocialToken, SocialApp
from action.models import UserData
from .pull_likes import get_myfacebook_likes
import requests
import sys


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


class LoadUserLikes(LoginRequiredMixin, View):
    """Module for previewing data from facebook."""
    template_name = 'load.html'

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
        tokens = SocialToken.objects.filter(
            account__user=request.user,
            account__provider='facebook'
        )

        user_data = UserData.objects.get_or_create(user=request.user)

        myfbgraph = facebook.GraphAPI(tokens[0].token)
        my_likes = get_myfacebook_likes(myfbgraph)
        user_data[0].likes = my_likes
        user_data[0].save()

        return render(request, self.template_name, self.get_context_data())
