from django.conf.urls import url
from logout import views

urlpatterns = [
    url(r'^$', views.LogoutView.as_view(), name='index'),
]