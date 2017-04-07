from django.conf.urls import url
from answers.views import WriteAnswerView

from questions.views import QuestionListAPIView, QuestionDetailView, QuestionCreateView, \
    QuestionAnswers, QuestionEditView, QuestionExploreAPI, QuestionExploreView, FollowQuestion, \
    UnFollowQuestion, GetQuestionFollowers, IsFollowingQuestion, AssignTopic, UnAssignTopic, UserQuestionsR2R

urlpatterns = [
    url(r'^$', QuestionListAPIView.as_view()),
    url(r'^create/', QuestionCreateView.as_view(), name='create'),
    url(r'^api/explore/', QuestionExploreAPI.as_view(), name='explore_questions_api'),
    url(r'^explore/', QuestionExploreView.as_view(), name='explore_questions'),
    url(r'^follow/', FollowQuestion.as_view(), name='follow_question'),
    url(r'^unfollow/', UnFollowQuestion.as_view(), name='unfollow_question'),
    url(r'^followers/', GetQuestionFollowers.as_view(), name='question_followers'),
    url(r'^is_following/', IsFollowingQuestion.as_view(), name='is_following_question'),
    url(r'^assign_topic/', AssignTopic.as_view(), name='assign_topic'),
    url(r'^unassign_topic/', UnAssignTopic.as_view(), name='unassign_topic'),
    url(r'^(?P<slug>[\w-]+)/$', QuestionDetailView.as_view(), name='q_detail'),
    url(r'^(?P<username>[\w-]+)/questions/$', UserQuestionsR2R.as_view(), name='user_questions'),
    url(r'^(?P<slug>[\w-]+)/answerit/$', WriteAnswerView.as_view(), name='answer_it'),
    url(r'^(?P<pk>\d+)/answers/$', QuestionAnswers.as_view(), name='answers'),
    url(r'^(?P<slug>[\w-]+)/edit/$', QuestionEditView.as_view(), name='edit_question'),
]

