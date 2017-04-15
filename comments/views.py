from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, JsonResponse
from django.shortcuts import render, render_to_response
from django.views import View
from rest_framework.generics import ListAPIView, CreateAPIView
from account.models import UserOtherDetails
from answers.models import Answer
from comments.models import Comment
from comments.pagination import CommentsPagination
from comments.serializers import CommentDetailsSerializer, CommentChildSerializer


class CreateComment(CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentDetailsSerializer


class RetrieveCommentsR2R(View):
    def get(self, request):
        if request.GET.get('answer'):
            try:
                comments = Comment.objects.filter(parent_answer_id=request.GET.get('answer'))
            except:
                raise ObjectDoesNotExist
        else:
            comments = Comment.objects.all()
        return render_to_response('comments/comments_frag.html',
                                  {'comments': comments, 'answer': request.GET.get('answer'), 'request': request})


class RetrieveCommentCommentsR2R(View):
    def get(self, request):
        print('comment id is ' + request.GET.get('comment'))
        if request.GET.get('comment'):
            try:
                comments = Comment.objects.filter(parent_id=request.GET.get('comment'))
            except:
                raise ObjectDoesNotExist
        else:
            comments = Comment.objects.all()
        print(comments)
        return render_to_response('comments/comment_comments_frag.html', {'comments': comments, 'request': request})


class RetrieveComments(ListAPIView):
    def get_queryset(self):
        if self.request.GET.get('answer'):
            try:
                answer = Answer.objects.get(pk=self.request.GET.get('answer'))
                comments = Comment.objects.filter(parent_answer=answer)
            except:
                raise ObjectDoesNotExist
        else:
            comments = Comment.objects.all()
        return comments

    serializer_class = CommentDetailsSerializer
    pagination_class = CommentsPagination


class PostComment(View):
    def get(self, request):
        return render(request, 'comments/comments.html')

    def post(self, request):
        comment_content = (request.POST['comment_content']).replace('"', '&quot')
        parent_id = request.POST['parent_id']
        parent_type = request.POST['parent_type']
        writer = request.user

        if int(parent_type) == 1:
            c = Comment(writer=writer, body=comment_content, parent_answer_id=parent_id)
            c.save()
            return JsonResponse(True, safe=False)
        if int(parent_type) == 2:
            c = Comment(writer=writer, body=comment_content, parent_id=parent_id)
            c.save()
            return JsonResponse(True, safe=False)
        return Http404()


class RetrieveChildrenComment(ListAPIView):
    def get_queryset(self):
        try:
            parent_id = self.kwargs['pk']
            comments = Comment.objects.filter(parent_id=parent_id)
        except:
            raise Http404
        return comments

    serializer_class = CommentChildSerializer


class Test(View):
    def get(self, request):
        return render(request, 'comments/comments.html');


class DeleteComment(View):
    def get(self, request):
        try:
            Comment.objects.get(pk=request.GET.get('comment')).delete()
        except Comment.DoesNotExist:
            pass
        return JsonResponse(True, safe=False)
