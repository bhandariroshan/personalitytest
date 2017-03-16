from django.db import models


class FacebookPost(models.Model):
    page_id = models.CharField(max_length=255, unique=True)
    posts = models.TextField(null=True, blank=True)
    page_info = models.TextField(null=True, blank=True)
    most_liked_post = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.page_id)
