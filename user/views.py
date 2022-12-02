from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from django.core.exceptions import ObjectDoesNotExist
from .forms import ProfileForm
from .decorators import redirect_mod

# Create your views here.


@login_required
@redirect_mod
def ProfileView(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return render(request, 'account/profile.html', {'form': ProfileForm()})
    else:
        profile = request.user.userprofile
        return render(request, 'account/profile.html', {'form': ProfileForm(instance=profile)})
