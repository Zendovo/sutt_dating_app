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
            profile = form.save(commit=False)

            age = profile.age
            fname = profile.first_name
            lname = profile.last_name
            gender = profile.gender
            pref = profile.preference
            about = profile.about
            image = profile.image
            try:
                gprofile = UserProfile.objects.get(user=request.user)
                gprofile.age = age
                gprofile.first_name = fname
                gprofile.last_name = lname
                gprofile.gender = gender
                gprofile.preference = pref
                gprofile.about = about
                gprofile.image = image
                gprofile.save()
            except ObjectDoesNotExist:
                UserProfile.objects.create(age=age, user=request.user, first_name=fname,
                                           last_name=lname, gender=gender, preference=pref, about=about, image=image)
        return redirect('/accounts/profile/')
    else:
        try:
            profile = request.user.userprofile
            return render(request, 'account/profile.html', {'form': ProfileForm(instance=profile)})
        except:
            return render(request, 'account/profile.html', {'form': ProfileForm()})
