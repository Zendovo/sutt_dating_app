from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound, HttpResponse
from user.models import NewUser, UserProfile, BlockList, ChatRequest, Reports
from django.db.models import Q
from user.decorators import moderator_required, profile_required


@login_required
@profile_required
def Index(request):
    query = request.GET.get('query')

    a = request.user.userprofile.blocklist.all()
    a_ids = []
    for i in a:
        a_ids.append(i.id)
    b = request.user.userprofile.blocked_by.all()
    b_ids = []
    for i in b:
        b_ids.append(i.id)
    if not query:
        query = ''
    profiles = UserProfile.objects.exclude(Q(id__in=a_ids) | Q(id__in=b_ids), id__exact=request.user.userprofile.id).filter(Q(first_name__icontains=query) | Q(last_name__icontains=query))
    paginator = Paginator(profiles, 2)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'sutt_dating_app/index.html', {'page_obj': page_obj})


@login_required
@profile_required
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
@profile_required
def BlockView(request):
    profiles = request.user.userprofile.blocklist.all()
    paginator = Paginator(profiles, 2)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'sutt_dating_app/blocklist.html', {'page_obj': page_obj})


@login_required
@profile_required
def Requests(request, request_id):
    # Accept User Request
    if request.method == 'POST':
        req = ChatRequest.objects.get(id=request_id)
        req.status = 'A'
        req.save()

        msg = req.message
        req.chatmessages_set.create(message=msg, sender=req.req_from)        

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
@profile_required
def RequestsView(request):
    if request.method == 'GET':
        requests = ChatRequest.objects.filter(
            req_to__id=request.user.userprofile.id, status__exact='U')
        paginator = Paginator(requests, 2)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'sutt_dating_app/requests.html', {'page_obj': page_obj})
    elif request.method == 'POST':
        request_to = int(request.POST['profile_id'])
        request_to = UserProfile.objects.get(id=request_to)
        message = request.POST['message']

        prior = ChatRequest.objects.filter(req_to=request.user.userprofile, req_from=request_to)
        if len(prior) > 0:
            prior[0].status = 'A'
            msg = prior[0].message
            prior[0].chatmessages_set.create(message=msg, sender=prior[0].req_from)
            prior[0].chatmessages_set.create(message=message, sender=request.user.userprofile)
            prior[0].save()
            return redirect('/chatroom/')

        ChatRequest.objects.create(
            req_from=request.user.userprofile, req_to=request_to, message=message)

        return redirect('/chatroom/')


@login_required
@moderator_required
def ModReportsView(request):
    if request.method == 'GET':
        reports = Reports.objects.all()
        paginator = Paginator(reports, 2)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'sutt_dating_app/reports.html', {'page_obj': page_obj})
    else:
        return HttpResponseNotFound


@login_required
@moderator_required
def ModReportsAction(request, report_id):
    if request.method == 'POST':
        action = request.POST['action']

        if action == 'delete_account':
            report = Reports.objects.get(id=report_id)
            user = NewUser.objects.get(id=report.reported.user.id)
            user.is_active = False
            user.save()
            report.delete()

        return HttpResponse(status=200)
    elif request.method == 'DELETE':
        Reports.objects.get(id=report_id).delete()
        return HttpResponse(status=200)


@login_required
@profile_required
def ReportsView(request):
    if request.method == 'POST':
        reported = int(request.POST['profile_id'])
        reported = UserProfile.objects.get(id=reported)
        message = request.POST['message']

        Reports.objects.create(
            message=message, reported=reported, reporter=request.user.userprofile)

        return redirect('/')
