from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.core.exceptions import ObjectDoesNotExist


def moderator_required(view_func):
    def wrap(request, *args, **kwargs):
        if request.user.is_moderator or request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('/')
    return wrap


def profile_required(view_func):
    def wrap(request, *args, **kwargs):
        if request.user.is_moderator:
            return HttpResponseRedirect('/mod')
        try:
            profile = request.user.userprofile
            final_verdict = True

            if not profile.first_name or profile.first_name.strip() == '':
                final_verdict = False
            elif not profile.age:
                final_verdict = False
            elif profile.image.url == 'default.jpg':
                final_verdict = False

            if final_verdict:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponseRedirect('/accounts/profile/')
        except ObjectDoesNotExist:
            return HttpResponseRedirect('/accounts/profile/')
    return wrap


def redirect_mod(view_func):
    def wrap(request, *args, **kwargs):
        if request.user.is_moderator or request.user.is_superuser:
            return HttpResponseRedirect('/mod/')
        else:
            return view_func(request, *args, **kwargs)
    return wrap