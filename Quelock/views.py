from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect, render_to_response
from django.utils.datastructures import MultiValueDictKeyError
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from Quelock.pagination import FeedsPagination
from account.models import UserFollowings, UserOtherDetails, Reports, AlreadyReadAnswers
from account.serializers import UserOtherDetailsSerializer
from answers.models import Answer, UpVotes
from answers.serializers import AnswerSerializer
from questions.models import QuestionImageUpload, Question, QuestionTopic, QuestionFollowing, ReadQuestions
from questions.serializers import QuestionSerializer
from topics.models import Topic, TopicFollowing
from topics.serializers import TopicSerializer


def user_profile(request, username):
    pass


def index(request):
    return render(request, 'home/index.html', {'feeds_active': 'active'})


@csrf_exempt
def upload(request):
    # folder = 'uploads'

    # uploaded_filename = request.FILES['image'].name
    uploaded_file = request.FILES['image']

    to_be_uploaded = QuestionImageUpload()
    to_be_uploaded.image = uploaded_file

    to_be_uploaded.save()
    image_url = to_be_uploaded.image.url

    # return JsonResponse(image_url, safe=False)

    return JsonResponse({'success': True, 'file': image_url})

    # try:
    #     os.mkdir(os.path.join(settings.PROJECT_DIR+'\\static\\images\\', folder))
    # except Exception as e:
    #     print(str(e))
    # full_filename = os.path.join(settings.PROJECT_DIR+'\\static\\images\\', folder, uploaded_filename)
    # fout = open(full_filename, 'wb+')
    #
    # for chunk in uploaded_file:
    #     fout.write(chunk)
    #
    # fout.close()
    # print(full_filename)
    # return JsonResponse({'success': True,
    #                      'file': settings.CURRENT_HOST + settings.UPLOADED_IMAGES_DIR + uploaded_filename})


class Follow(View):
    def post(self, request):
        user_that_clicked = request.user
        follows = request.GET.get('follows')
        is_following = User.objects.get(pk=follows)
        user_that_clicked = UserOtherDetails.objects.get(user=user_that_clicked)
        follows = UserOtherDetails.objects.get(user=is_following)
        if UserFollowings.objects.filter(user=user_that_clicked, is_following=follows).exists():
            return JsonResponse(True, safe=False)
        else:
            u = UserFollowings(user=user_that_clicked, is_following=follows)
            u.save()
            return JsonResponse(True, safe=False)


class UnFollow(View):
    def post(self, request):
        user_that_clicked = request.user
        follows = request.GET.get('follows')
        try:
            user1 = UserOtherDetails.objects.get(user=User.objects.get(username=user_that_clicked))
            user2 = UserOtherDetails.objects.get(user=User.objects.get(pk=follows))
            user_following = UserFollowings.objects.get(user=user1, is_following=user2)
            user_following.delete()
        except UserFollowings.DoesNotExist:
            user_following = None
        return JsonResponse(True, safe=False)


class IsFollowing(View):
    def post(self, request):
        user = request.user
        is_following = request.GET.get('is_following')
        try:
            user1 = UserOtherDetails.objects.get(user=User.objects.get(username=user))
            user2 = UserOtherDetails.objects.get(user=User.objects.get(pk=is_following))
            f = UserFollowings.objects.filter(user=user1, is_following=user2)
        except UserFollowings.DoesNotExist:
            f = None
        if f:
            return JsonResponse(True, safe=False)
        else:
            return JsonResponse(False, safe=False)


class Report(View):
    def get(self, request):
        report_type = request.GET.get('type')
        r_s = report_type
        type_id = request.GET.get('type_id')
        if report_type is 'A':
            report_type = 'Answer'
        if report_type is 'Q':
            report_type = 'Question'
        if report_type is 'U':
            report_type = 'User'
        else:
            report_type = ''

        reasons = [
            {'header': 'Spam', 'text': '3rd party Advertisement'},
            {'header': 'Does not answer the question', 'text': 'Answer does not correlate with question'},
            {'header': 'Poorly Constructed', 'text': 'Bad grammar, formatting or spelling'},
            {'header': 'Bad Image/Answer Body', 'text': 'Image/Answer depicts decayed moral value'}
        ]
        context = {'type': report_type, 'type_sing': r_s, 'reasons': reasons, 'type_id': type_id}
        return render(request, 'report.html', context)

    def post(self, request):
        report_type = request.POST['type']
        type_id = request.POST['type_id']
        reason = request.POST['reason']
        next_url = request.GET.get('next')

        r = Reports(type=report_type, type_id=type_id, message=reason)
        r.save()
        return redirect(next_url)


class Search(View):
    def get(self, request):
        search_term = request.GET.get('search_term')
        sort_type = request.GET.get('sort_type')
        context = {'search_term': search_term, 'sort_type': sort_type}
        return render(request, 'home/search_results.html', context)


class SearchAPI(APIView):
    def get(self, request):
        search_term = request.GET.get('search_term')
        sort_type = int(request.GET.get('sort_type'))
        page = int(request.GET['page'])

        splited_term = search_term.split()

        if sort_type == 1:
            q = Question.objects.filter(
                Q(title__icontains=search_term) |
                Q(question_details__icontains=search_term)
            ).distinct().order_by('-no_of_answers')
            pagination_class = Paginator(q, 5)
            q = pagination_class.page(page)
            serializer = QuestionSerializer(q, many=True)
            return Response(serializer.data)

        if sort_type == 2:
            p = UserOtherDetails.objects.filter(
                Q(user__username__icontains=search_term) |
                Q(user__first_name__icontains=search_term) |
                Q(user__last_name__icontains=search_term)
            ).distinct()
            pagination_class = Paginator(p, 2)
            p = pagination_class.page(page)
            serializer = UserOtherDetailsSerializer(p, many=True)
            return Response(serializer.data)

        if sort_type == 3:
            t = Topic.objects.filter(
                Q(title__icontains=search_term) |
                Q(desc__icontains=search_term)
            ).distinct()
            pagination_class = Paginator(t, 3)
            t = pagination_class.page(page)
            serializer = TopicSerializer(t, many=True)
            return Response(serializer.data)
        return Response(None)


class AskSearchR2R(View):
    def get(self, request):
        search_term = request.GET.get('search_term')
        q = Question.objects.filter(
            Q(title__icontains=search_term) |
            Q(question_details__icontains=search_term)
        ).distinct().order_by('-no_of_answers')
        return render_to_response('ask-search.html', {'questions': q})


class FeedsAnswersAPI(ListAPIView):
    serializer_class = AnswerSerializer
    pagination_class = FeedsPagination

    def get_queryset(self):
        # Answers under topics user is following
        topics_followed = TopicFollowing.objects.filter(user_id=self.request.user.id).values('follows')
        questions = QuestionTopic.objects.filter(under_id__in=topics_followed).values('question')
        answers = Answer.objects.filter(question_id__in=questions).order_by('-time-written')

        # Answers written by people you follow
        user_following = UserFollowings.objects.filter(user_id=self.request.user.id).values('is_following')
        answers2 = Answer.objects.filter(writer_id__in=user_following).order_by('-time_written').order_by('time-written')

        # Answers upvoted by people you follow
        upvotes = UpVotes.objects.filter(user_id__in=user_following).select_related().values('answer').order_by('-date')
        answers3 = Answer.objects.filter(id__in=upvotes).order_by('time-written')

        # Combining the result sets
        all_answers = answers | answers2 | answers3

        already_read = AlreadyReadAnswers.objects.filter(user_id=self.request.user.id).values('answer')

        try:
            already_loaded = self.request.GET['loaded']
        except MultiValueDictKeyError:
            already_loaded = []

        all_answers = all_answers.exclude(id__in=already_read).exclude(id__in=already_loaded)
        all_answers = all_answers.distinct().order_by('-time-written')[:300]

        return all_answers


class FeedAnswerR2R(View):
    def get(self, request):
        topics_followed = TopicFollowing.objects.filter(user_id=request.user.id).values('follows')
        questions = QuestionTopic.objects.filter(under_id__in=topics_followed).values('question')
        answers = Answer.objects.filter(question_id__in=questions).select_related()

        # Answers written by people you follow
        user_following = UserFollowings.objects.filter(user_id=request.user.id).values('is_following')
        answers2 = Answer.objects.filter(writer_id__in=user_following).select_related()

        # Answers upvoted by people you follow
        upvotes = UpVotes.objects.filter(user_id__in=user_following).select_related().values('answer')
        answers3 = Answer.objects.filter(id__in=upvotes).select_related()

        # Answers in questions followed by those you follow
        qf = QuestionFollowing.objects.filter(user_id=request.user).values('question')
        answers4 = Answer.objects.filter(question_id__in=qf)

        # Combining the result sets
        all_answers = answers | answers2 | answers3 | answers4

        already_read = AlreadyReadAnswers.objects.filter(user_id=request.user.id).values('answer')

        if int(request.GET['page']) == 1:
            all_answers = all_answers.exclude(id__in=already_read).exclude(writer_id=request.user.id)
        else:
            all_answers = all_answers.exclude(writer_id=request.user.id)

        all_answers = all_answers.distinct().order_by('-time_written')[:300]

        p = Paginator(all_answers, 5)
        p = p.page(request.GET['page'])

        if p.has_next():
            next_page = None
        else:
            next_page = 1

        return render_to_response('answers/answer_item.html',
                                  {'answers': p, 'request': request, 'next_page': next_page})


class FeedQuestionsAPI(ListAPIView):
    serializer_class = QuestionSerializer

    def get_queryset(self):
        user_following = UserFollowings.objects.filter(user_id=self.request.user.id).values('is_following')
        # Questions followed by people you follow
        question_ff = QuestionFollowing.objects.filter(user_id__in=user_following).values('question')
        questions = Question.objects.filter(id__in=question_ff).order_by('?')

        topics_followed = TopicFollowing.objects.filter(user_id=self.request.user.id).values('follows')
        questions2 = QuestionTopic.objects.filter(under_id__in=topics_followed).values('question')
        questions2 = Question.objects.filter(id__in=questions2).order_by('?')

        questions = questions | questions2

        try:
            loaded_questions = self.request.GET['loaded']
        except MultiValueDictKeyError:
            loaded_questions = []

        read_questions = ReadQuestions.objects.filter(user_id=self.request.user.id).values('question')
        questions.exclude(id__in=read_questions).exclude(id__in=loaded_questions).distinct()

        return questions


class FeedAnswersView(View):
    def get(self, request):
        return render(request, 'home/index.html')

    def post(self, request):
        question = request.POST['question']
        try:
            anonymous = request.POST['anonymous']
        except:
            anonymous = 0

        author = request.user

        q = Question(title=question, anonymous=anonymous, question_details='', author=author)
        q.save()
        print(q.slug)
        return redirect('/questions/' + q.slug)


class FeedQuestionsView(View):
    def get(self, request):
        return render(request, 'home/index.html')
