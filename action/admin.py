from django.contrib import admin

# Register your models here.
from action.models import UserData, UserLikes, PageSettings


@admin.register(UserData)
class UserDataAdmin(admin.ModelAdmin):
    list_display = ('user','likes_pulled',)

@admin.register(UserLikes)
class UserLikesAdmin(admin.ModelAdmin):
    list_display = ('user',)

@admin.register(PageSettings)
class PageSettingsAdmin(admin.ModelAdmin):
    list_display = ('pageid',)
