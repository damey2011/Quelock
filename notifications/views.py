from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from notifications.models import Notification


class GetUserNotifications(View):
    def get(self, request):
        n = Notification.objects.filter(owner=request.user, read_status=False)


class MarkAsRead(View):
    def get(self, request):
        notification_id = request.GET.get('notification')
        n = Notification.objects.get(pk=notification_id)
        n.read_status = True
        n.save()
        return JsonResponse(True, safe=False)


class MarkAllAsRead(View):
    def get(self, request):
        n = Notification.objects.filter(owner=request.user, read_status=False)
        for note in n:
            note.read_status = True
            note.save()
