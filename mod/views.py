from django.shortcuts import render
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound
from user.decorators import moderator_required
from .tables import UserProfilesTables
from user.models import UserProfile

# Create your views here.
@method_decorator(login_required, name='dispatch')
@method_decorator(moderator_required, name='dispatch')
class ModView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'mod/index.html')

@method_decorator(login_required, name='dispatch')
@method_decorator(moderator_required, name='dispatch')
class ProfilesView(View):
    def get(self, request, *args, **kwargs):
        table = UserProfilesTables(UserProfile.objects.all())
        table.paginate(page=request.GET.get('page', 1), per_page=1)
        return render(request, 'mod/profiles.html', {'table': table})
