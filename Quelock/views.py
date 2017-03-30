from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from account.models import UserFollowings, UserOtherDetails, Reports
from account.pagination import UserOtherDetailsPagination
from account.serializers import UserOtherDetailsSerializer
from questions.models import QuestionImageUpload, Question
from questions.serializers import QuestionSerializer
from topics.models import Topic
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
