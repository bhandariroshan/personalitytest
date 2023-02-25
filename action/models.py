from __future__ import unicode_literals

from django.db import models
from fbstats.users.models import User
from django.contrib.postgres.fields import JSONField
# Create your models here.


class UserData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    ver_code = models.TextField(null=True, blank=True)
    mobile_ver_flg = models.BooleanField(default=False)
    email_ver_flg = models.BooleanField(default=False)

    pre_charity_org = models.IntegerField(default=0)

    ad_view_total = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.TextField(null=True, blank=True)
    last_upd = models.DateTimeField(auto_now_add=True)
    last_upd_by = models.TextField(null=True, blank=True)

    likes_pulled = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user.first_name) + " " + str(self.user.last_name)


class UserLikes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    like = JSONField(null=True, blank=True)

    def __str__(self):
        return str(self.user.first_name) + " " + str(self.user.last_name)

 
class  PageSettings (models.Model):
    """History of PageConversation."""
    pageid = models.TextField(null=True, blank=True)
    access_token = models.TextField(null=True, blank=True)


class  PageConversation (models.Model):
    """History of PageConversation."""
    conversation_replied = models.BooleanField(default=False)
    reply_message = models.TextField(null=True, blank=True)
    conversation = JSONField(null=True, blank=True)

        
