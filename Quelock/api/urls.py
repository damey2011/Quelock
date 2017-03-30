from django.conf.urls import url
from Quelock.api.views import HomeContentAPI, QuestionAPIView

urlpatterns = [
    url(r'^$', HomeContentAPI.as_view()),
    url(r'^(?P<slug>\w+)$', QuestionAPIView.as_view()),
]
