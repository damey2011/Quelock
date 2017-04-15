from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from django.db.models import Q
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from account.forms import AccountUpdateForm
from account.models import UserOtherDetails, UserFollowings
from account.pagination import FollowPagination, UserOtherDetailsPagination
from account.serializers import UserOtherDetailsSerializer, FollowingSerializer, FollowersSerializer
from answers.models import Answer
from questions.models import Question
from topics.models import TopicFollowing, Topic
from topics.serializers import TopicSerializer


class ProfileView(View):
    def get(self, request, username):
        requested_user = User.objects.get(username=username).profile
        requested_user.profile_no_of_views += 1
        requested_user.save()
        try:
            # user1 = UserOtherDetails.objects.get(user=User.objects.get(username=request.user))
            user1 = request.user.profile
            # user2 = UserOtherDetails.objects.get(user=User.objects.get(username=username))
            user2 = User.objects.get(username=username).profile
            i = UserFollowings.objects.filter(user=user2, is_following=user1).exists()
            u = UserFollowings.objects.get(user=user1, is_following=user2)
        except:
            u = None
            i = False
        if u is not None:
            is_following = True
        else:
            is_following = False
        a = Answer.objects.filter(writer=requested_user).count()
        b = Question.objects.filter(author=requested_user.user).count()

        context = {'req_user': requested_user, 'is_following': is_following, 'no_of_answers': a, 'no_of_questions': b,
                   'follows_back': i, 'account_active': 'active'}
        return render(request, 'profile/profile.html', context)


class AllProfilesView(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = UserOtherDetails.objects.all()
    serializer_class = UserOtherDetailsSerializer


class ProfileUpdateView(View):
    def get(self, request, username):
        req_user = User.objects.get(username=username).profile
        form = AccountUpdateForm(instance=req_user)
        return render(request, 'profile/update_profile.html', {'form': form, 'account_active': 'active'})

    def post(self, request, username):
        req_user = User.objects.get(username=username).profile
        form = AccountUpdateForm(request.POST or None, request.FILES or None, instance=req_user)
        if form.is_valid():
            form.save()
            return redirect('/profile/' + req_user.user.username)
        return HttpResponse("An error occurred")


class RetrieveFollowing(ListAPIView):
    def get_serializer_context(self):
        return {'request': self.request}

    pagination_class = FollowPagination
    serializer_class = FollowingSerializer

    def get_queryset(self, *args, **kwargs):
        user = self.kwargs['username']
        queryset_list = UserFollowings.objects.all()
        if user:
            queryset_list = queryset_list.filter(
                Q(user__user__username__exact=user)
            ).distinct()
        return queryset_list


class RetrieveFollowers(ListAPIView):
    def get_serializer_context(self):
        return {'request': self.request}

    pagination_class = FollowPagination
    serializer_class = FollowersSerializer

    def get_queryset(self, *args, **kwargs):
        user = self.kwargs['username']
        queryset_list = UserFollowings.objects.all()
        if user:
            queryset_list = queryset_list.filter(
                Q(is_following__user__username__exact=user)
            ).distinct()
        return queryset_list


class UserFollowers(View):
    def get(self, request, username):
        requested_user = UserOtherDetails.objects.get(user=User.objects.get(username=username))
        requested_user.profile_no_of_views += 1
        requested_user.save()
        try:
            user1 = UserOtherDetails.objects.get(user=User.objects.get(username=request.user))
            user2 = UserOtherDetails.objects.get(user=User.objects.get(username=username))
            i = UserFollowings.objects.filter(user=user2, is_following=user1).exists()
            u = UserFollowings.objects.get(user=user1, is_following=user2)
        except:
            u = None
            i = False
        if u is not None:
            is_following = True
        else:
            is_following = False
        a = len(Answer.objects.filter(writer=requested_user))
        b = len(Question.objects.filter(author=requested_user.user))
        context = {'req_user': requested_user, 'is_following': is_following, 'no_of_answers': a, 'no_of_questions': b,
                   'follows_back': i, 'account_active': 'active'}
        return render(request, 'profile/followers.html', context)


class RetrieveFollowedTopics(ListAPIView):
    def get_queryset(self, *args, **kwargs):
        req_user = self.request.GET.get('req_user')
        req_user = User.objects.get(username=req_user)
        req_user = UserOtherDetails.objects.get(user=req_user)

        user = self.request.GET.get('user')
        user = User.objects.get(username=user)
        user = UserOtherDetails.objects.get(user=user)

        if req_user == user:
            queryset = TopicFollowing.objects.filter(user=user).values('follows')
            queryset = Topic.objects.filter(pk__in=queryset)
        else:
            user_foll = TopicFollowing.objects.filter(user=user).values('follows')
            req_user_foll = TopicFollowing.objects.filter(user=req_user).values('follows')
            queryset = Topic.objects.filter(pk__in=req_user_foll).exclude(pk__in=user_foll)
        return queryset

    serializer_class = TopicSerializer


class ExplorePeopleAPI(ListAPIView):
    def get_queryset(self):
        profile = self.request.user.profile
        uf1 = UserFollowings.objects.filter(user=profile).values('is_following')
        uf = UserOtherDetails.objects.all().exclude(pk__in=uf1).exclude(pk=profile.user.id).order_by('?')
        return uf

    serializer_class = UserOtherDetailsSerializer
    pagination_class = UserOtherDetailsPagination


class ExplorePeopleView(View):
    def get(self, request):
        return render(request, 'profile/explore.html', {'people_active': 'active', 'explore_active': 'active'})