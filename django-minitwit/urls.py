from django.conf.urls import patterns, include, url
from minitwit.views import TimelineView, PublicTimelineView, UserTimelineView, \
    FollowUserView, UnfollowUserView, AddMessageView, LogoutView, \
    UserRegisterView
from django.contrib import admin


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$',
        TimelineView.as_view(),
        name='timeline'),
    url(r'^login/$',
        'django.contrib.auth.views.login',
        kwargs={'template_name': 'login.html'},
        name='login'),
    url(r'^logout/$',
        LogoutView.as_view(),
        name='logout'),
    url(r'^register/$',
        UserRegisterView.as_view(),
        name='register'),
    url(r'^public/$',
        PublicTimelineView.as_view(),
        name='public_timeline'),
    url(r'^add_message/$',
        AddMessageView.as_view(),
        name='add_message'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^(?P<username>\w+)/$',
        UserTimelineView.as_view(),
        name='user_timeline'),
    url(r'^(?P<username>\w+)/follow/$',
        FollowUserView.as_view(),
        name='follow_user'),
    url(r'^(?P<username>\w+)/unfollow/$',
        UnfollowUserView.as_view(),
        name='unfollow_user'),
)
