from django.conf.urls import url
from notifications import views

urlpatterns = [
    # url(r'^$', views.GetUserNotifications.as_view(), name='all_notifications'),
    url(r'^all/', views.GetUserNotifications.as_view(), name='all_ajax_notifications'),
    url(r'^get_count/', views.GetUnreadNotificationsCount.as_view(), name='notifications_count'),
    url(r'^mark/', views.MarkAsRead.as_view(), name='mark_single'),
    url(r'^mark_all/', views.MarkAllAsRead.as_view(), name='mark_all_as_read'),
]
