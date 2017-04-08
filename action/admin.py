from django.contrib import admin

# Register your models here.
from action.models import UserData, UserLikes


@admin.register(UserData)
class UserDataAdmin(admin.ModelAdmin):
    list_display = ('user','likes_pulled',)

@admin.register(UserLikes)
class UserLikesAdmin(admin.ModelAdmin):
    list_display = ('user',)
