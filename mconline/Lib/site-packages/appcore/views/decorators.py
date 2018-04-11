from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from appcore.conf import settings


def anonymous_required(function):
    """Redirect to user profile if user is already logged-in"""

    def wrapper(*args, **kwargs):
        if args[0].user.is_authenticated():
            url = settings.ANONYMOUS_REQUIRED_REDIRECT_URL
            return HttpResponseRedirect(reverse(url))
        return function(*args, **kwargs)

    return wrapper
