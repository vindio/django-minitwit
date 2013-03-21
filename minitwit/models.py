from django.db import models
from django.contrib.auth.models import User


class Follower(models.Model):
    who = models.ForeignKey(User, related_name='following', null=False)
    whom = models.ForeignKey(User, related_name='followers', null=False)

    class Meta:
        unique_together = (('who', 'whom'),)

    def __unicode__(self):
        return "%s follows %s" % (self.who.username,
                                  self.whom.username)


class Message(models.Model):
    author = models.ForeignKey(User, related_name='messages', null=False)
    text = models.TextField(null=False, blank=False)
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-pub_date',)

    def __unicode__(self):
        return ('Message from "%s" %s' %
                (self.author, self.pub_date.strftime("%d/%m/%Y @ %H:%M")))
