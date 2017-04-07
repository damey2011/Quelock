from django.conf.urls import url
from account.views import ProfileView, ProfileUpdateView, AllProfilesView, RetrieveFollowers, RetrieveFollowing, \
    ExplorePeopleView, ExplorePeopleAPI, RetrieveFollowedTopics, UserFollowers

urlpatterns = [
    url(r'^$', AllProfilesView.as_view(), name='all_profiles'),
    url(r'^api/explore/', ExplorePeopleAPI.as_view(), name='explore_people_api'),
    url(r'^explore/', ExplorePeopleView.as_view(), name='explore_people'),
    url(r'^topics_followed/', RetrieveFollowedTopics.as_view(), name='followed_topics'),
    url(r'^(?P<username>\w+)$', ProfileView.as_view(), name='profile'),
    url(r'^(?P<username>\w+)/followings/api$', RetrieveFollowing.as_view(), name='followings_api'),
    url(r'^(?P<username>\w+)/followers/api$', RetrieveFollowers.as_view(), name='followers_api'),
    url(r'^(?P<username>\w+)/followings$', RetrieveFollowing.as_view(), name='user_followings'),
    url(r'^(?P<username>\w+)/followers$', UserFollowers.as_view(), name='user_followers'),
    url(r'^(?P<username>\w+)/update$', ProfileUpdateView.as_view(), name='profile_update')
]
