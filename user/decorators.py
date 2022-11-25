from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.core.exceptions import PermissionDenied


def moderator_required(view_func):
    def wrap(request, *args, **kwargs):
        if request.user.is_moderator or request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('/')
    return wrap
