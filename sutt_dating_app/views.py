from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound, HttpResponse
from user.models import UserProfile, BlockList, ChatRequest


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


@login_required
def BlockView(request):
    profiles = request.user.userprofile.blocklist.all()
    paginator = Paginator(profiles, 2)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'sutt_dating_app/blocklist.html', {'page_obj': page_obj})


@login_required
def Requests(request, request_id):
    # Accept User Request
    if request.method == 'POST':
        req = ChatRequest.objects.get(id=request_id)
        req.status = 'A'
        req.save()

        return HttpResponse(status=200)
    # Decline User Request
    elif request.method == 'DELETE':
        req = ChatRequest.objects.get(id=request_id)
        req.status = 'D'
        req.save()

        return HttpResponse(status=200)
    else:
        return HttpResponseNotFound


@login_required
def RequestsView(request):
    if request.method == 'GET':
        requests = ChatRequest.objects.filter(
            req_to__id=request.user.userprofile.id)
        paginator = Paginator(requests, 2)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'sutt_dating_app/requests.html', {'page_obj': page_obj})
    elif request.method == 'POST':
        print(request.POST)
        request_to = int(request.POST['profile_id'])
        request_to = UserProfile.objects.get(id=request_to)
        message = request.POST['message']

        # TODO:
        # before creation check if the user has a pending chat request from the same user
        # in that case send the opening message in the chat and accept the request
        ChatRequest.objects.create(
            req_from=request.user.userprofile, req_to=request_to, message=message)

        return redirect('/chat_pending/')
