from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import View

from rest_framework.generics import ListAPIView, RetrieveAPIView
from account.models import UserFollowings, UserOtherDetails
from account.serializers import UserOtherDetailsSerializer
from answers.models import Answer
from answers.serializers import AnswerSerializer
from questions.models import QuestionTopic
from topics.forms import TopicCreateUpdateForm

from topics.models import Topic, TopicFollowing
from topics.pagination import TopicAnswersPagination, TopicPagination
from topics.serializers import TopicSerializer, TopicFollowingSerializer


class TopicsListAPIView(ListAPIView):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer


class TopicDetailAPIView(RetrieveAPIView):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer


class TopicListView(View):
    def get(self, request):
        return render(request, 'topic/topic_list.html', {'topics': Topic.objects.all()})

    def post(self, request):
        pass


class TopicDetailView(View):
    def get(self, request, slug):
        topic = Topic.objects.get(slug=slug)
        questions_under = QuestionTopic.objects.filter(under=topic)
        no_following_topic = (TopicFollowing.objects.filter(follows=topic).count())
        total_answers = 0
        for question in questions_under:
            total_answers += Answer.objects.filter(question=question.question).count()
        user = UserOtherDetails.objects.get(user=request.user)
        follows = topic
        tf = TopicFollowing.objects.filter(user=user, follows=follows).exists()
        context = {'topic': topic,
                   'no_of_questions_under': len(questions_under),
                   'no_following_topic': no_following_topic,
                   'total_answers': total_answers, 'is_following': tf}
        return render(request, 'topic/topic.html', context)

    def post(self, request):
        pass


class TopicCreateView(View):
    def get(self, request):
        form = TopicCreateUpdateForm
        return render(request, 'topic/create_topic.html', {'form': form, 'explore_active': 'active'})

    def post(self, request):
        form = TopicCreateUpdateForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save()
            return redirect('/topics')
        return HttpResponse("An error occurred")


class TopicUpdateView(View):
    def get(self, request, pk):
        t = Topic.objects.get(pk=pk)
        form = TopicCreateUpdateForm(instance=t)
        return render(request, 'topic/create_topic.html', {'form': form})

    def post(self, request, pk):
        t = Topic.objects.get(pk=pk)
        form = TopicCreateUpdateForm(request.POST or None, request.FILES or None, instance=t)
        if form.is_valid():
            form.save()
            return redirect('/topics')
        return HttpResponse("An error occurred")


def topic_create_success(request):
    return render(request, 'topic/topic_create_success.html', {'explore_active': 'active'})


def follow_topic(request):
    t = Topic.objects.get(pk=request.GET.get('topic'))
    try:
        tf = TopicFollowing.objects.get(user=UserOtherDetails.objects.get(user=request.user), follows=t)
    except ObjectDoesNotExist:
        tf = TopicFollowing(user=UserOtherDetails.objects.get(user=request.user), follows=t)
        tf.save()
        return JsonResponse(True, safe=False)


def unfollow_topic(request):
    try:
        t = Topic.objects.get(pk=request.GET.get('topic'))
        tf = TopicFollowing.objects.filter(user=UserOtherDetails.objects.get(user=request.user), follows=t)
        if tf.exists():
            tf.delete()
        return JsonResponse(True, safe=False)
    except ObjectDoesNotExist:
        return JsonResponse(False, safe=False)


def iffollow_topic_ajax(request):
    try:
        t = Topic.objects.get(pk=request.GET.get('topic'))
        tf = TopicFollowing.objects.get(user=UserOtherDetails.objects.get(user=request.user), follows=t)
    except ObjectDoesNotExist:
        tf = None
    if tf is not None:
        return JsonResponse(True, safe=False)
    else:
        return JsonResponse(False, safe=False)


class RelatedTopics(ListAPIView):
    def get_queryset(self):
        profile = UserOtherDetails.objects.get(user=self.request.user)
        tf = TopicFollowing.objects.filter(user=profile).values('follows')
        t = Topic.objects.exclude(pk__in=tf).order_by('?')[:10]
        return t

    serializer_class = TopicSerializer


class RecentTopicAnswers(ListAPIView):
    def get_queryset(self):
        topic_id = self.request.GET.get('topic')
        topic = Topic.objects.get(pk=topic_id)
        q = QuestionTopic.objects.filter(under=topic).values('question')
        a = Answer.objects.filter(question__in=q).order_by('-date_written', '-time_written')
        return a

    serializer_class = AnswerSerializer
    pagination_class = TopicAnswersPagination


class ExploreTopicAPI(ListAPIView):
    def get_queryset(self):
        profile = UserOtherDetails.objects.get(user=self.request.user)
        tf = TopicFollowing.objects.filter(user=profile).values('follows')
        t = Topic.objects.exclude(pk__in=tf).order_by('?')
        return t

    serializer_class = TopicSerializer
    pagination_class = TopicPagination


class ExploreTopicView(View):
    def get(self, request):
        return render(request, 'topic/explore.html', {'topic_active': 'active', 'explore_active': 'active'})


class CommonInterestUsers(ListAPIView):
    def get_queryset(self):
        try:
            user = UserOtherDetails.objects.get(user=self.request.user)
            uf = UserFollowings.objects.filter(user=user).values('is_following')
            t = Topic.objects.get(pk=self.request.GET.get('topic'))
            tf = TopicFollowing.objects.filter(follows=t).exclude(user__in=uf).order_by('?').exclude(user=user).values(
                'user')[:10]
            users = UserOtherDetails.objects.filter(pk__in=tf)
            return users
        except ObjectDoesNotExist:
            return None

    serializer_class = UserOtherDetailsSerializer
    # pagination_class = CommonUserPagination


class SearchTopic(ListAPIView):
    def get_queryset(self):
        keyword = self.request.GET.get('keyword')
        matches = Topic.objects.filter(
            Q(title__icontains=keyword) |
            Q(desc__icontains=keyword)
        ).distinct()
        return matches
    serializer_class = TopicSerializer
