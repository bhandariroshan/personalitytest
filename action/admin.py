from django.contrib import admin

# Register your models here.
from action.models import UserData, UserLikes

admin.site.register(UserData)
admin.site.register(UserLikes)