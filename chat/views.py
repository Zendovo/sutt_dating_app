from django.shortcuts import render
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound
from user.models import ChatRequest
from django.db.models import Q
from user.decorators import profile_required

# Create your views here.
@method_decorator(login_required, name='dispatch')
@method_decorator(profile_required, name='dispatch')
class Index(View):
    def get(self, request, *args, **kwargs):
        all_chats = ChatRequest.objects.filter(Q(req_from=request.user.userprofile) | Q(req_to=request.user.userprofile), status__exact='A')
        for chat in all_chats:
            chat.unread = chat.chatmessages_set.filter(~Q(sender=request.user.userprofile), seen=False).count()

        return render(request, 'chat/index.html', {
            'chats': all_chats,
        })


@method_decorator(login_required, name='dispatch')
@method_decorator(profile_required, name='dispatch')
class ChatRoom(View):
    def get(self, request, *args, **kwargs):
        chat_id = self.kwargs['chat_id']
        current_chat = ChatRequest.objects.get(id=chat_id, status__exact='A')

        if not current_chat:
            return HttpResponseNotFound
        
        all_chats = ChatRequest.objects.filter(Q(req_from=request.user.userprofile) | Q(req_to=request.user.userprofile), status__exact='A')
        for chat in all_chats:
            chat.unread = chat.chatmessages_set.filter(~Q(sender=request.user.userprofile), seen=False).count()

        messages = current_chat.chatmessages_set.all()
        return render(request, 'chat/chatroom.html', {
            'chat_id': chat_id,
            'chats': all_chats,
            'current_chat': current_chat,
            'msgs': messages,
        })