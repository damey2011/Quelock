from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import connection
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, render_to_response
from django.views.generic import View

from rest_framework.generics import ListAPIView, RetrieveAPIView
from account.models import UserFollowings, UserOtherDetails
from account.serializers import UserOtherDetailsSerializer
from answers.models import Answer
from questions.models import QuestionTopic
from topics.forms import TopicCreateUpdateForm

from topics.models import Topic, TopicFollowing
from topics.pagination import TopicPagination
from topics.serializers import TopicSerializer


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
        user = request.user.profile
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
            return redirect('/topics/')
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
    if TopicFollowing.objects.get_or_create(user=request.user.profile, follows_id=request.GET.get('topic')):
        return JsonResponse(True, safe=False)
    else:
        return JsonResponse(True, safe=False, status=500)
        # try:
        #     tf = TopicFollowing.objects.get(user=request.user, follows_id=request.GET.get('topic'))
        # except ObjectDoesNotExist:
        #     tf = TopicFollowing(user=request.user, follows_id=request.GET.get('topic'))
        #     tf.save()
        # return JsonResponse(True, safe=False)


def unfollow_topic(request):
    try:
        tf = TopicFollowing.objects.filter(user=request.user, follows_id=request.GET.get('topic'))
        if tf.exists():
            tf.delete()
        return JsonResponse(True, safe=False)
    except ObjectDoesNotExist:
        return JsonResponse(False, safe=False)


def iffollow_topic_ajax(request):
    try:
        tf = TopicFollowing.objects.get(user=request.user, follows_id=request.GET.get('topic'))
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


# class RecentTopicAnswers(ListAPIView):
#     def get_queryset(self):
#         topic_id = self.request.GET.get('topic')
#         q = QuestionTopic.objects.filter(under_id=topic_id).values('question')
#         a = Answer.objects.filter(question__in=q).order_by('-date_written', '-time_written')
#         return a
#
#     serializer_class = AnswerSerializer
#     pagination_class = TopicAnswersPagination


class RecentTopicAnswers(View):
    def get(self, request):
        topic_id = request.GET.get('topic')
        try:
            page = request.GET.get('page')
        except PageNotAnInteger:
            page = 1
        q = QuestionTopic.objects.filter(under_id=topic_id).values('question')
        a = Answer.objects.filter(question__in=q).select_related().order_by('-time_written')
        p = Paginator(a, 1)
        try:
            p = p.page(page)
        except PageNotAnInteger:
            p = p.page(1)

        try:
            next_page = p.next_page_number()
        except EmptyPage:
            next_page = None
            return HttpResponse(None)

        return render_to_response('answers/answer_item.html',
                                  {'answers': p, 'request': request, 'next_page': next_page})


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


class GettingStartedRecommendedTopics(View):
    def get(self, request):
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(question_id) AS question_count, under_id FROM "
                           "questions_questiontopic GROUP BY under_id ORDER BY question_count DESC LIMIT 25")

            row = cursor.fetchall()
        t = Topic.objects.none()
        for item in row:
            t = t | Topic.objects.filter(pk=item[1])

        tf = TopicFollowing.objects.filter(user_id=request.user.id).values('follows')

        t = t.exclude(pk__in=tf)

        return render_to_response('topic/new_user_topic_suggest.html', {'topics': t})


class CheckUserNoOfTopicsFollowed(View):
    def get(self, request):
        no = TopicFollowing.objects.filter(user_id=request.user.id).count()

        if no < 15:
            return JsonResponse(False, safe=False)
        else:
            return JsonResponse(True, safe=False)