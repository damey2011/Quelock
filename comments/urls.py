from django.conf.urls import url
from comments import views

urlpatterns = [
    url(r'^$', views.RetrieveComments.as_view(), name='all'),
    url(r'^retrieve_answer_comments/', views.RetrieveCommentsR2R.as_view(), name='answer_comments'),
    url(r'^retrieve_comment_comments/', views.RetrieveCommentCommentsR2R.as_view(), name='comment_comments'),
    url(r'^delete/', views.DeleteComment.as_view(), name='delete_comment'),
    url(r'^create/', views.CreateComment.as_view(), name='create'),
    url(r'^test/', views.Test.as_view(), name='test'),
    url(r'^post/', views.PostComment.as_view(), name='post'),
    url(r'^(?P<pk>\d+)/children', views.RetrieveChildrenComment.as_view(), name='children_comment'),

]
