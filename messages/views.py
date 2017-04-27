from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, render_to_response

# Create your views here.
from django.views import View
from Quelock.tasks import message_notify
from messages.models import Conversation, ConversationReplies


class Messages(View):
    def get(self, request):
        return render(request, 'messages/messages.html')


class MessageUser(View):
    def post(self, request):
        sender = request.user.id
        receiver = request.POST['receiver']
        message = request.POST['message']

        if int(sender) < int(receiver):
            user_1 = sender
            user_2 = receiver
        else:
            user_1 = receiver
            user_2 = sender

        try:
            c = Conversation.objects.get(user_1_id=user_1, user_2_id=user_2)
        except Conversation.DoesNotExist:
            c = Conversation(user_1_id=user_1, user_2_id=user_2)
            c.save()

        cr = ConversationReplies(conv=c, reply=message, user=request.user)
        cr.save()

        message_notify.delay(sender_id=sender, conv_rep_id=cr.id)
        return JsonResponse(True, safe=False)


class ReplyMessage(View):
    def post(self, request):
        sender = request.user
        conv_id = request.POST['conv_id']
        message = request.POST['message']

        cr = ConversationReplies(conv_id=conv_id, reply=message, user=sender)
        cr.save()

        message_notify.delay(sender_id=sender.id, conv_rep_id=cr.id)

        return JsonResponse(True, safe=False)


class RetrieveMessageThreads(View):
    def get(self, request):
        c = Conversation.objects.filter(
            Q(user_1_id=request.user.id) |
            Q(user_2_id=request.user.id)
        ).values('id')

        cr = ConversationReplies.objects.filter(conv_id__in=c).select_related().distinct().order_by('-time')

        cf = (cr.order_by('conv').values('conv').distinct())

        c_list = []

        for c in cf:
            c_list.append(ConversationReplies.objects.filter(conv_id=c['conv']).order_by('-time').first())

        c_list.sort(key=lambda x: x.time, reverse=True)

        return render_to_response('messages/fragments/message-threads.html', {'threads': c_list, 'request': request})


class RetrieveMessageThread(View):
    def get(self, request, conv_id):
        print(conv_id)
        cr = ConversationReplies.objects.filter(conv_id=conv_id)
        return render_to_response('messages/fragments/message-thread.html', {'messages': cr, 'request': request})
