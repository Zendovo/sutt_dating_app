from django.core.paginator import Paginator
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound
from user.models import UserProfile
from django.core.exceptions import ObjectDoesNotExist

@login_required
def Index(request):
    profiles = UserProfile.objects.all()
    paginator = Paginator(profiles, 2) # Show 25 contacts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'sutt_dating_app/index.html', {'page_obj': page_obj})