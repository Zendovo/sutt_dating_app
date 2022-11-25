from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound
from user.models import UserProfile, BlockList
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q


@login_required
def Index(request):
    profiles = UserProfile.objects.raw('SELECT * FROM user_userprofile uu LEFT JOIN user_blocklist ub ON uu.id IN (ub.blocked_id, ub.blocker_id) AND %s IN (ub.blocked_id, ub.blocker_id) WHERE ub.id IS NULL AND uu.id <> %s;', [
                                       request.user.userprofile.id, request.user.userprofile.id])
    paginator = Paginator(profiles, 2)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'sutt_dating_app/index.html', {'page_obj': page_obj})


@login_required
def BlockUser(request, profile_id):
    if request.method == 'POST':
        # block user
        # blocked = NewUser.objects.get(id=request.POST['block_id'])
        request.user.userprofile.blocklist.add(
            UserProfile.objects.get(id=profile_id))
        # block = BlockList(blocked=blocked, blocker=request.user)
        # block.save()
        return redirect('/block')
    elif request.method == 'DELETE':
        test = BlockList.objects.filter(blocked=UserProfile.objects.get(
            id=profile_id), blocker=request.user.userprofile).delete()
        return redirect('/block')


@ login_required
def BlockView(request):
    profiles = request.user.userprofile.blocklist.all()
    paginator = Paginator(profiles, 2)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'sutt_dating_app/blocklist.html', {'page_obj': page_obj})


@ login_required
def ChatRequest(request):
    if request.method == 'POST':
        # get user id from the body
        target = request.POST['id']

        # get user id from the authenticated user
        user = request.user.id

        # insert a row in the requests table
        return
    else:
        # get all the chat requests
        return render(request, 'user/requests', {})


@ login_required
def ChatRequestList(request):
    if request.method == 'GET':
        # get user id from the authenticated user
        user = request.user.id

        # get the list of requests from the requests table
        return
    else:
        return HttpResponseNotFound()
