from django.conf.urls import url

from topics import views

urlpatterns = [
    url(r'^$', views.TopicListView.as_view()),
    url(r'^create/$', views.TopicCreateView.as_view()),
    url(r'^created/', views.topic_create_success, name='topic_created'),
    url(r'^follow/', views.follow_topic, name='follow_topic'),
    url(r'^unfollow/', views.unfollow_topic, name='unfollow_topic'),
    url(r'^iffollow/', views.iffollow_topic_ajax, name='iffollow_topic'),
    url(r'^recent_answers/', views.RecentTopicAnswers.as_view(), name='recent_answers'),
    url(r'^related/', views.RelatedTopics.as_view(), name='related_topics'),
    url(r'^common_interest_users/', views.CommonInterestUsers.as_view(), name='common_interest'),
    url(r'^api/explore', views.ExploreTopicAPI.as_view()),
    url(r'^explore/', views.ExploreTopicView.as_view(), name='explore_topic'),
    url(r'^search/', views.SearchTopic.as_view(), name='search_topic'),
    url(r'^(?P<slug>[\w-]+)/$', views.TopicDetailView.as_view()),
    url(r'^(?P<pk>[0-9]+)/edit', views.TopicUpdateView.as_view()),
    url(r'^api/$', views.TopicsListAPIView.as_view()),
    url(r'^api/(?P<pk>[0-9]+)$', views.TopicDetailAPIView.as_view()),
]

