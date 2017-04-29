from django.conf.urls import url
from answers.views import AnswerView, EditAnswerView, AnswersAPIView, DeleteAnswerView, \
    BookmarkAnswer, UnBookmarkAnswer, CheckUpvoted, Downvote, Upvote, CheckDownvoted, CheckBookmarked, ArchivedAnswers,\
    TrendingAnswersByUpvotes, TrendingAnswersByInteractions, GetUpvoters, Thank, SuggestEdit, \
    UserAnswersR2R, AddNewView, DeleteArchive

urlpatterns = [
    url(r'^$', AnswersAPIView.as_view()),
    url(r'^delete/', DeleteAnswerView.as_view()),
    url(r'^edit/$', EditAnswerView.as_view()),
    url(r'^archived/$', ArchivedAnswers.as_view(), name='archived'),
    url(r'^delete_archive/$', DeleteArchive.as_view(), name='delete_archived'),
    url(r'^check_if_bookmarked/', CheckBookmarked.as_view()),
    url(r'^bookmark_answer/', BookmarkAnswer.as_view()),
    url(r'^un_bookmark_answer/', UnBookmarkAnswer.as_view()),
    url(r'^check_upvoted/', CheckUpvoted.as_view()),
    url(r'^check_downvoted/', CheckDownvoted.as_view()),
    url(r'^upvote/', Upvote.as_view()),
    url(r'^downvote/', Downvote.as_view()),
    url(r'^upvoters/', GetUpvoters.as_view()),
    url(r'^trending/by_upvotes', TrendingAnswersByUpvotes.as_view()),
    url(r'^trending/', TrendingAnswersByInteractions.as_view()),
    url(r'^thank/', Thank.as_view(), name='thank'),
    url(r'^suggest_edit/', SuggestEdit.as_view(), name='suggest_edit'),
    url(r'^add_view/', AddNewView.as_view(), name='add_new_view'),
    url(r'^(?P<pk>\d+)/$', AnswerView.as_view(), name='answer'),
    url(r'^(?P<username>\w+)/', UserAnswersR2R.as_view()),
]
