from hashlib import md5
from django import template
import copy

register = template.Library()

@register.filter(name='gravatar')
def gravatar_url(value, arg):
    """Return the gravatar image for the given email address."""
    size = arg or 80
    return 'http://www.gravatar.com/avatar/%s?d=identicon&s=%s' % \
            (md5(value.strip().lower().encode('utf-8')).hexdigest(), size)


@register.simple_tag()
def form_field_errors(form):
    try:
        tmp = copy.deepcopy(form)
        tmp.errors.pop('__all__', None)
        return tmp.errors
    except:
        return ''
