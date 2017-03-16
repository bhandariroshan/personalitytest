from __future__ import unicode_literals

from django.db import models
from fbstats.users.models import User
# Create your models here.


class UserData(models.Model):
    name = models.CharField(max_length=1000, null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User)

    def __str__(self):
        return str(self.name)
