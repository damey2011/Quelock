from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import F
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, render_to_response
from django.views import View
from rest_framework.generics import ListAPIView
from Quelock.tasks import upvote_notify, decr_no_of_upvotes, addAnswerView, thanks_create_and_notify, follow_question
from account.models import UserOtherDetails, UserFollowings, AlreadyReadAnswers
from account.pagination import UserOtherDetailsPagination
from account.serializers import UserOtherDetailsSerializer
from answers.models import Answer, Bookmark, UpVotes, DownVotes, Thanks, SuggestEdits, AnonymousAnswerWriters
from answers.pagination import UserAnswerPagination, TrendingAnswersPagination
from answers.serializers import AnswerSerializer
from questions.models import Question


class AnswersAPIView(ListAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer


class AnswerView(View):
    def get(self, request, pk):
        answer = Answer.objects.get(pk=pk)
        try:
            b = Bookmark.objects.get(user=request.user, answer_id=pk)
            already_upvoted = UpVotes.objects.filter(user=request.user, answer_id=pk)
            already_downvoted = DownVotes.objects.filter(user=request.user, answer_id=pk)
        except:
            b = None
            already_upvoted = None
            already_downvoted = None
        try:
            user1 = request.user
            user2 = answer.writer.user.id
            i = UserFollowings.objects.filter(user_id=user1, is_following_id=user2)
        except:
            i = None

        context = {'answer': answer, 'is_bookmarked': b, 'already_upvoted': already_upvoted,
                   'already_downvoted': already_downvoted, 'is_following': i, 'feeds_active': 'active'}
        return render(request, 'answers/answer.html', context)


class WriteAnswerView(View):
    def get(self, request, slug):
        page_title = 'Write Answer'
        question = Question.objects.get(slug=slug)
        return render(request, 'answers/create_answer.html', {'page_title': page_title, 'question': question})

    def post(self, request, slug):
        answer_question = Question.objects.get(slug=slug)
        body = request.POST['details']

        writer = UserOtherDetails.objects.get(user=request.user)

        question = answer_question

        answer = Answer()
        answer.question_string = answer_question.title
        answer.body = body.replace("'", "&apos;")
        answer.writer = writer
        answer.question = question
        answer.author = writer

        if request.POST.get('anonymous'):
            answer.anonymous = True

        answer.save()

        if answer.anonymous:
            AnonymousAnswerWriters(answer=answer, user=request.user).save()

        answer_question.no_of_answers += 1
        answer_question.save()

        writer.increase_no_of_answers()
        writer.save()

        return redirect('/questions/' + question.slug)


class EditAnswerView(View):
    def get(self, request):
        page_title = 'Edit Answer'
        answer = Answer.objects.get(pk=request.GET.get('answer'))
        return render(request, 'answers/edit_answer.html', {'page_title': page_title, 'answer': answer})

    def post(self, request):
        body = request.POST['details']
        answer = Answer.objects.get(pk=request.GET.get('answer'))
        answer.body = body.replace("'", '&apos;')
        answer.save()
        return redirect('/answers/' + str(answer.id))


class UserAnswerAPIView(ListAPIView):
    serializer_class = AnswerSerializer
    pagination_class = UserAnswerPagination

    def get_queryset(self):
        req_user = User.objects.get(username=self.kwargs['username'])
        try:
            a = Answer.objects.filter(writer=req_user.userotherdetails)
            if self.request.user != req_user:
                a = a.exclude(anonymous=True)
        except Answer.DoesNotExist:
            a = None
        return a


class UserAnswersR2R(View):
    def get(self, request, username):
        req_user = User.objects.get(username=username)
        try:
            a = Answer.objects.filter(writer_id=req_user.id).order_by('time_written')
            if self.request.user != req_user:
                a = a.exclude(anonymous=True)
        except Answer.DoesNotExist:
            a = None
        p = Paginator(a, 3)
        p = p.page(request.GET.get('page'))

        if p.has_next():
            next_page = None
        else:
            next_page = 1

        return render_to_response('answers/answer_item.html',
                                  {'answers': p, 'request': request, 'next_page': next_page})


class DeleteAnswerView(View):
    def post(self, request):
        answer_to_be_del = Answer.objects.get(pk=request.POST['answer'])
        answer_to_be_del.delete()

        q = answer_to_be_del.question
        q.no_of_answers -= 1
        q.save()

        return JsonResponse(True, safe=False)


class ArchivedAnswers(View):
    def get(self, request):
        try:
            b = Bookmark.objects.filter(user=request.user)
            return render(request, 'bookmarks/bookmarks.html', {'answers': b, 'archive_active': 'active'})
        except:
            b = None
        return HttpResponse('You have to log in to access this page bruhh')


class BookmarkAnswer(View):
    def post(self, request):
        b = Bookmark()
        b.user = request.user
        b.answer = Answer.objects.get(pk=request.GET.get('answer'))
        b.save()
        return JsonResponse(True, safe=False)


class UnBookmarkAnswer(View):
    def post(self, request):
        b = Bookmark.objects.filter(user=request.user, answer=request.GET.get('answer'))
        b.delete()
        return JsonResponse(True, safe=False)


class CheckUpvoted(View):
    def post(self, request):
        a = Answer.objects.get(pk=request.GET.get('answer'))
        try:
            u = UpVotes.objects.get(answer=a, user=request.user)
        except:
            u = None
        if u is not None:
            return JsonResponse(True, safe=False)
        else:
            return JsonResponse(False, safe=False)


class CheckDownvoted(View):
    def post(self, request):
        a = Answer.objects.get(pk=request.GET.get('answer'))
        try:
            d = DownVotes.objects.get(answer=a, user=request.user)
        except:
            d = None
        if d is not None:
            return JsonResponse(True, safe=False)
        else:
            return JsonResponse(False, safe=False)


class Upvote(View):
    def post(self, request):
        a = Answer.objects.get(pk=request.GET.get('answer'))
        global reply
        if str(request.GET.get('action')) == 'upvote':
            UpVotes(answer=a, user=request.user).save()
            upvote_notify.delay(request.GET.get('answer'), request.user.id)
            reply = True
        if str(request.GET.get('action')) == 'r_upvote':
            u = UpVotes.objects.filter(answer=a, user=request.user)
            a.no_of_upvotes -= 1
            a.save()
            decr_no_of_upvotes.delay(a.id)
            for i in u:
                i.delete()
            reply = True
        return JsonResponse(reply, safe=False)


class Downvote(View):
    def post(self, request):
        a = Answer.objects.get(pk=request.GET.get('answer'))
        global reply
        if str(request.GET.get('action')) == 'downvote':
            d = DownVotes(answer=a, user=request.user)
            a.no_of_downvotes += 1
            a.save()
            d.save()
            reply = True
        if str(request.GET.get('action')) == 'r_downvote':
            d = DownVotes.objects.filter(answer=a, user=request.user)
            a.no_of_downvotes -= 1
            a.save()
            for i in d:
                i.delete()
            reply = True
        return JsonResponse(reply, safe=False)


class CheckBookmarked(View):
    def post(self, request):
        try:
            b = Bookmark.objects.get(user=request.user, answer=Answer.objects.get(pk=request.GET.get('answer')))
        except:
            b = None
        if b is not None:
            return JsonResponse(True, safe=False)
        else:
            return JsonResponse(False, safe=False)


class GetUpvoters(ListAPIView):
    def get_queryset(self):
        u = UpVotes.objects.filter(answer=int(self.request.GET.get('answer'))).values('user')
        p = UserOtherDetails.objects.filter(user__in=u)
        return p

    serializer_class = UserOtherDetailsSerializer
    pagination_class = UserOtherDetailsPagination


class TrendingAnswersByUpvotes(ListAPIView):
    def get_queryset(self):
        user = UserOtherDetails.objects.get(user=self.request.user)
        viewed_answers = AlreadyReadAnswers.objects.filter(user=user).values('answer')
        a = Answer.objects.all().order_by('-no_of_upvotes').exclude(pk__in=viewed_answers)
        return a

    serializer_class = AnswerSerializer


class TrendingAnswersByInteractions(ListAPIView):
    def get_queryset(self):
        user = UserOtherDetails.objects.get(user=self.request.user)
        viewed_answers = AlreadyReadAnswers.objects.filter(user=user).values('answer')
        a = Answer.objects.all().order_by((F('no_of_views') + F('no_of_comments') + F('no_of_upvotes')).desc()).exclude(
            pk__in=viewed_answers)[:150]
        return a

    serializer_class = AnswerSerializer
    pagination_class = TrendingAnswersPagination


class TrendingAnswersView(View):
    def get(self, request):
        return render(request, 'home/trending.html', {'trending_active': 'active'})


class Thank(View):
    def post(self, request):
        answer_id = request.GET.get('answer')
        user_id = request.user.id
        thanks_create_and_notify.delay(answer_id, user_id)
        return JsonResponse(True, safe=False)


class SuggestEdit(View):
    def post(self, request):
        answer_id = request.GET.get('answer')
        answer = Answer.objects.get(pk=answer_id)
        if SuggestEdits.objects.filter(suggester=request.user, original_writer=answer.writer.user,
                                       answer=answer).exists():
            return JsonResponse(False, safe=False)
        else:
            s = SuggestEdits(suggester=request.user, original_writer=answer.writer.user, answer=answer)
            s.save()
        return JsonResponse(True, safe=False)


class AddNewView(View):
    def get(self, request):
        answer_id = request.GET.get('answer')
        addAnswerView.delay(int(request.user.id), int(answer_id))
        return JsonResponse(True, safe=False)
