from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from Quelock import views
from Quelock import settings
from Quelock.views import Report, Search, SearchAPI
from account.views import RetrieveMessage
from account.views import RetrieveMessageThreads
from answers.views import TrendingAnswersView

urlpatterns = [
    url(r'^$', views.index, name='index_home'),
    url(r'^admin/', admin.site.urls),
    url(r'^signup/', include('registration.urls')),
    # Question API
    url(r'^questions/', include('questions.urls'), name='question'),
    url(r'^answers/', include('answers.urls')),
    url(r'^login/', include('login.urls'), name='login'),
    url(r'^logout/', include('logout.urls'), name='logout'),
    url(r'^profile/', include('account.urls')),
    url(r'^topics/', include('topics.urls')),
    url(r'^comments/', include('comments.urls'), name='comments'),
    url(r'^upload/', views.upload, name='upload'),
    url(r'^api/', include('Quelock.api.urls')),
    url(r'^follow/', views.Follow.as_view()),
    url(r'^unfollow/', views.UnFollow.as_view()),
    url(r'^is_following/', views.IsFollowing.as_view()),
    url(r'^trending/', TrendingAnswersView.as_view(), name='trending_by_interactions'),
    url(r'^report/', Report.as_view(), name='report'),
    url(r'^search/', Search.as_view(), name='search'),
    url(r'^ajax/search/$', SearchAPI.as_view(), name='search_api'),
    url(r'^messages$', RetrieveMessageThreads.as_view(), name='message_threads'),
    url(r'^messages/user/(?P<pk>\d+)/$', RetrieveMessage.as_view(), name='message_thread'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
