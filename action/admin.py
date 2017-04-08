from django.contrib import admin

# Register your models here.
from action.models import UserData, UserLikes


@admin.register(UserData)
class TermResultAdmin(admin.ModelAdmin):
    list_display = ('user','likes_pulled',)
    search_fields = ('user',)

@admin.register(UserLikes)
class TermResultAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('user')
