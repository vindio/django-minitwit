from django.contrib import admin
from models import Message, Follower
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin


class MessageAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'author', 'pub_date')
    list_filter = ('author', 'pub_date')
    list_select_related = True
    search_fields = ('author__username', 'text')
admin.site.register(Message, MessageAdmin)


class FollowerAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'who', 'whom')
    list_filter = ('who', 'whom')
    list_select_related = True
    search_fields = ('who__username', 'whom__username')
admin.site.register(Follower, FollowerAdmin)


class TwUserAdmin(UserAdmin):
    list_display = ('__unicode__', 'email', 'is_staff', 'count_messages',
                    'count_following', 'count_followers')

    def count_messages(self, user):
        return user.messages.count()
    count_messages.short_description = 'Messages'

    def count_followers(self, user):
        return user.followers.count()
    count_followers.short_description = 'Followers'

    def count_following(self, user):
        return user.following.count()
    count_following.short_description = 'Following'


admin.site.unregister(User)
admin.site.register(User, TwUserAdmin)
