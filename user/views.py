from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound
from .models import UserProfile
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.


@login_required
def ProfileView(request):
    if request.method == 'POST':
        user_id = request.user.id
        age = request.POST['age']
        fname = request.POST['fname']
        lname = request.POST['lname']
        try:
            profile = UserProfile.objects.get(id=user_id)
            profile.age = age
            profile.first_name = fname
            profile.last_name = lname
            profile.save()
        except ObjectDoesNotExist:
            UserProfile.objects.create(age=age, user=request.user, first_name=fname, last_name=lname)
        return redirect('/accounts/profile')
    else:
        user_id = request.user.id
        try:
            profile = UserProfile.objects.get(id=user_id)
            return render(request, 'account/profile.html', {'user': request.user, 'profile': profile})
        except ObjectDoesNotExist:
            return render(request, 'account/profile.html', {'user': request.user, 'profile': {}})
            
