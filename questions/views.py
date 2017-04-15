from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import render, redirect, render_to_response
from django.utils.datastructures import MultiValueDictKeyError
from django.views import View
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from account.models import UserOtherDetails
from answers.models import Answer

from questions.models import Question, QuestionTopic, QuestionFollowing, AnonymousQuestionsWriters, ReadQuestions, \
    AnswerRequest
from questions.pagination import MyTestPagination, ExploreQuestionPagination
from .serializers import QuestionSerializer


class QuestionListAPIView(ListAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    pagination_class = MyTestPagination


class QuestionDetailsAPIView(RetrieveAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class QuestionListView(View):
    def get(self, request):
        pass

    def post(self, request):
        pass


class QuestionDetailView(View):
    def get(self, request, slug):
        question = Question.objects.get(slug=slug)
        try:
            writer = request.user.profile
            user_has_answered_question_already = Answer.objects.filter(
                writer=writer, question=question)
        except:
            writer = None
            user_has_answered_question_already = None

        if QuestionFollowing.objects.filter(user=request.user, question=question).exists():
            user_follows = True
        else:
            user_follows = False

        question_tags = QuestionTopic.objects.filter(question=question).select_related('under')

        if ReadQuestions.objects.filter(user=request.user, question=question).exists():
            pass
        else:
            ReadQuestions(user=request.user, question=question).save()

        context = {'question': question,
                   'user_has_answered_question_already': user_has_answered_question_already, 'explore_active': 'active',
                   'user_follows': user_follows, 'tags': question_tags}
        return render(request, 'question/question.html', context)

    def post(self, request):
        pass


class QuestionDetailAPIView(APIView):
    def get(self, request, slug):
        question = Question.objects.get(slug=slug)
        serializer = QuestionSerializer(question)
        return Response(serializer.data)

    def post(self, request):
        pass


class RelatedQuestionsView(View):
    def get(self, request):
        pass

    def post(self, request):
        pass


class QuestionCreateView(View):
    def get(self, request):
        return render(request, 'question/create_question.html')

    def post(self, request):
        title = request.POST['title']
        details = request.POST['details'].replace("'", '&apos;')
        author = request.user

        question = Question(title=title, question_details=details)

        try:
            question.anonymous = request.POST['anonymous']
        except:
            pass

        # if request.POST['anonymous']:
        #     question.anonymous = True

        question.author = author
        question.save()

        if question.anonymous:
            AnonymousQuestionsWriters(question=question, user=request.user).save()

        write_profile = author.profile
        write_profile.no_of_questions += 1
        write_profile.save()

        return redirect('/questions/' + str(question.slug))


# class QuestionAnswers(ListAPIView):
#     serializer_class = AnswerSerializer
#
#     def get_queryset(self):
#         try:
#             answers = Answer.objects.filter(question_id=self.kwargs['pk'])
#         except:
#             answers = None
#         return answers


class QuestionAnswers(View):
    def get(self, request, pk):
        try:
            answers = Answer.objects.filter(question_id=pk)
            total = answers.count()
        except:
            answers = None
        return render_to_response('answers/answer_item.html',
                                  {'answers': answers, 'request': request, 'total_answers': total})


class QuestionEditView(View):
    def get(self, request, slug):
        question = Question.objects.get(slug=slug)
        question.question_details = question.question_details
        return render(request, 'question/edit_question.html', {'question': question})

    def post(self, request, slug):
        title = request.POST['title']
        details = request.POST['details']

        question = Question.objects.get(slug=slug)
        question.title = title
        question.question_details = details.replace("'", '&apos;')

        question.save(force_update=True)

        return redirect('/questions/' + str(question.slug))


# class UserQuestions(ListAPIView):
#     pagination_class = UserQuestionPagination
#     serializer_class = QuestionSerializer
#
#     def get_queryset(self, *args, **kwargs):
#         user = self.kwargs['username']
#         try:
#             q = Question.objects.filter(author=User.objects.get(username=user))
#         except Question.DoesNotExist:
#             q = None
#         return q


class UserQuestionsR2R(View):
    def get(self, request, username):
        user = self.kwargs['username']
        try:
            q = Question.objects.filter(author=User.objects.get(username=user))
        except Question.DoesNotExist:
            q = None
        return render_to_response('question/fragments/question_item.html', {'questions': q, 'request': request})


class QuestionExploreAPI(ListAPIView):
    def get_queryset(self):
        u = self.request.user.profile
        aq = Answer.objects.filter(writer=u).values('question')
        q = Question.objects.all().exclude(pk__in=aq)
        return q

    serializer_class = QuestionSerializer
    pagination_class = ExploreQuestionPagination


class QuestionExploreView(View):
    def get(self, request):
        return render(request, 'question/explore.html', {'questions_active': 'active', 'explore_active': 'active'})


class FollowQuestion(View):
    def get(self, request):
        q = request.GET.get('question')
        q = int(q)
        try:
            if QuestionFollowing.objects.filter(user=request.user, question_id=q).exists():
                pass
            else:
                qf = QuestionFollowing(user=request.user, question_id=q)
                qf.save()
            return JsonResponse(True, safe=False)
        except ObjectDoesNotExist:
            return JsonResponse(False, safe=False)


class UnFollowQuestion(View):
    def get(self, request):
        q = request.GET.get('question')
        q = int(q)
        try:
            qf = QuestionFollowing.objects.filter(user=request.user, question_id=q)
            qf.delete()
            return JsonResponse(True, safe=False)
        except ObjectDoesNotExist:
            return JsonResponse(False, safe=False)


class GetQuestionFollowers(ListAPIView):
    def get_queryset(self):
        try:
            q = Question.objects.get(pk=self.request.GET.get('question'))
            qf = QuestionFollowing.objects.filter(question=q).values('user')
            u = UserOtherDetails.objects.filter(pk__in=qf)
            return u
        except Exception:
            return None

    serializer_class = QuestionSerializer


class IsFollowingQuestion(View):
    def get(self, request):
        try:
            qf = QuestionFollowing.objects.filter(user=request.user, question_id=request.GET.get('question')).exists()
            return JsonResponse(qf, safe=False)
        except ObjectDoesNotExist:
            return JsonResponse(False, safe=False)


class AssignTopic(View):
    def post(self, request):
        if QuestionTopic.objects.filter(question_id=request.GET.get('question'),
                                        under_id=request.GET.get('topic')).exists():
            pass
        else:
            qt = QuestionTopic()
            qt.question_id = request.GET.get('question')
            qt.under_id = request.GET.get('topic')
            qt.save()
        return JsonResponse(True, safe=False)


class UnAssignTopic(View):
    def post(self, request):
        qt = QuestionTopic.objects.filter(question_id=request.GET.get('question'), under_id=request.GET.get('topic'))
        if qt.exists():
            qt.delete()
        return JsonResponse(True, safe=False)


class RequestUserAnswersToQuestions(View):
    def post(self, request):
        try:
            topics_list = request.POST['topics[]']
        except MultiValueDictKeyError:
            topics_list = []

        ar = AnswerRequest.objects.filter(requester=request.user, question=request.POST['question']).values(
                'receipient')

        if len(topics_list) > 0:
            q = QuestionTopic.objects.filter(under__in=topics_list).distinct().values('question')

            # Dev env
            aw = Answer.objects.filter(question_id__in=q).select_related().values('writer').distinct()[:25]
            users = User.objects.filter(id__in=aw).exclude(id__in=ar).exclude(pk=request.user.id).prefetch_related()

            # Production envir, does not work in dev env
            # aw = Answer.objects.filter(question_id__in=q).select_related().values('writer').distinct('writer')[:25]

        else:
            users = User.objects.all().exclude(id__in=ar).order_by('?')[:20]

        return render_to_response('question/request_answers.html',
                                      {'users': users, 'request': request, 'sent_already': ar.count()})


class SendAnswerRequest(View):
    def post(self, request):
        question = request.POST['question']
        requester = request.POST['requester']
        receipient = request.POST['receipient']

        AnswerRequest(requester_id=requester, receipient_id=receipient, question_id=question).save()
        return JsonResponse(True, safe=False)


class RemoveAnswerRequest(View):
    def post(self, request):
        question = request.POST['question']
        requester = request.POST['requester']
        receipient = request.POST['receipient']

        AnswerRequest.objects.get(requester_id=requester, receipient_id=receipient, question_id=question).delete()
        return JsonResponse(True, safe=False)
