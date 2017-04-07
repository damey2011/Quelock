from django.conf.urls import url
from messages import views

urlpatterns = [
    url(r'^$', views.Messages.as_view(), name='messages_front'),
    url(r'^send/$', views.MessageUser.as_view(), name='message_user'),
    url(r'^reply/$', views.ReplyMessage.as_view(), name='reply'),
    url(r'^ajax/messages/threads/$', views.RetrieveMessageThreads.as_view(), name='message_threads'),
    url(r'^ajax/messages/threads/(?P<conv_id>\d+)/$', views.RetrieveMessageThread.as_view(), name='message_thread')
]
