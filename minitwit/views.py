from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse_lazy, resolve
from django.db.models import Q
from django.dispatch import receiver
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.signals import user_logged_in
from django.views.generic import ListView, View
from django.views.generic.edit import CreateView
from minitwit.models import Message, Follower
from minitwit.forms import UserCreationForm

PAGE_SIZE = 5


class BaseTimelineView(ListView):
    template_name = 'timeline.html'
    context_object_name = 'twits'
    paginate_by = PAGE_SIZE

    def get_context_data(self, **kwargs):
        context = super(BaseTimelineView, self).get_context_data(**kwargs)
        context['endpoint'] = resolve(self.request.path).url_name
        if getattr(self, 'title', False):
            context['title'] = self.title
        elif getattr(self, 'get_title', False):
            context['title'] = self.get_title()
        return context


class TimelineView(BaseTimelineView):
    """Shows a users timeline or if no user is logged in it will
    redirect to the public timeline. This timeline shows the user's
    messages as well as all the messages of followed users.
    """
    title = "My timeline"

    @method_decorator(login_required(login_url=
                                     reverse_lazy('public_timeline')))
    def dispatch(self, request, *args, **kwargs):
        self.user = request.user
        return super(TimelineView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Message.objects.select_related().filter(
            Q(author=self.user) |
            Q(author__in=self.user.following.values_list('whom',
                                                         flat=True)))


class PublicTimelineView(BaseTimelineView):
    """Displays the latest messages of all users."""
    
    title = "Public timeline"

    def get_queryset(self):
        return Message.objects.select_related()


class UserTimelineView(BaseTimelineView):
    """Display's a users tweets."""

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.user = request.user
        self.profile_user = get_object_or_404(User,
                            username__iexact=kwargs['username'])
        return super(UserTimelineView, self).dispatch(request,
                                                      *args, **kwargs)

    def get_queryset(self):
        return self.profile_user.messages.select_related().all()

    def get_context_data(self, **kwargs):
        context = super(UserTimelineView, self).get_context_data(**kwargs)
        context['followed'] = Follower.objects.filter(who=self.user,
                              whom=self.profile_user).exists()
        context['profile_user'] = self.profile_user
        return context

    def get_title(self):
        return "%s's timeline" % self.profile_user.username


class FollowUserView(View):
    """Adds the current user as follower of the given user."""
    redirect_url_name = 'user_timeline'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.who = request.user
        self.whom = get_object_or_404(User,
                                      username__iexact=kwargs['username'])
        return super(FollowUserView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        try:
            follower = Follower(who=self.who, whom=self.whom)
            follower.save()
            messages.success(request,
                             'You are now following "%s"' % self.whom)
        except:
            messages.error(request,
                           'Error. Yet you are not following "%s".'
                           % self.whom)
        return HttpResponseRedirect(reverse_lazy(self.redirect_url_name,
                                                 args=(self.whom,)))


class UnfollowUserView(View):
    """Removes the current user as follower of the given user."""
    redirect_url_name = 'user_timeline'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.who = request.user
        self.whom = get_object_or_404(User,
                                      username__iexact=kwargs['username'])
        return super(UnfollowUserView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        try:
            follower = Follower.objects.get(who=self.who, whom=self.whom)
            follower.delete()
            messages.success(request,
                             'You are no longer following "%s"' % self.whom)
        except:
            messages.error(request,
                           'Error unfollowing. It\'s possible that you are '
                           'still following "%s."' % self.whom)
        return HttpResponseRedirect(reverse_lazy(self.redirect_url_name,
                                                 args=[self.whom]))


class AddMessageView(View):
    """Registers a new message for the user."""
    redirect_url_name = 'timeline'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(AddMessageView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        try:
            msg = Message(author=request.user, text=request.POST['text'])
            msg.save()
            messages.success(request, 'Your message was recorded')
        except:
            messages.error(request, 'Error. Your message was not recorded')
        return HttpResponseRedirect(reverse_lazy(self.redirect_url_name))


class LogoutView(View):
    """Logs the user out."""
    redirect_url = reverse_lazy('public_timeline')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, 'You were logged out')
        return HttpResponseRedirect(self.redirect_url)


class UserRegisterView(CreateView):
    """Registers the user."""
    model = User
    template_name = 'register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super(UserRegisterView, self).form_valid(form)
        messages.success(self.request, 'You were successfully registered ' \
                         'and can login now')
        return response


@receiver(user_logged_in)
def user_logged_in_cb(sender, request, user, **kwargs):
    messages.success(request, 'You are logged in as "%s"' % user)
