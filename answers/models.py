from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.http import Http404
from account.models import UserOtherDetails
from comments.models import Comment
from questions.models import Question
from topics.models import Topic


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True)
    writer = models.ForeignKey(UserOtherDetails, on_delete=models.SET('Anonymous'), null=True)
    date_written = models.DateField()
    time_written = models.TimeField()
    body = models.TextField()
    no_of_upvotes = models.IntegerField(null=True, default=0)
    no_of_downvotes = models.IntegerField(null=True, default=0)
    no_of_views = models.IntegerField(null=True, default=0)
    no_of_comments = models.IntegerField(null=True, default=0)
    edited = models.IntegerField(null=True, default=0)
    anonymous = models.BooleanField(default=False)

    def __str__(self):
        return self.question.title

    def getComments(self):
        try:
            return Comment.objects.filter(parent_answer=self).count()
        except Exception as e:
            print(e)

    def isUpvoted(self, user):
        try:
            return UpVotes.objects.filter(user=user, answer=self).exists()
        except:
            return False

    def isDownvoted(self, user):
        try:
            return DownVotes.objects.filter(user=user, answer=self).exists()
        except:
            return False

    def isArchived(self, user):
        try:
            return Bookmark.objects.filter(user=user, answer=self).exists()
        except:
            return False

    def hasThanked(self, user):
        try:
            return Thanks.objects.filter(user=user, answer=self).exists()
        except:
            return False

    def hasSuggested(self, user):
        try:
            return SuggestEdits.objects.filter(suggester=user, answer=self).exists()
        except:
            return False


class UpVotes(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_user_details(self):
        try:
            u = UserOtherDetails.objects.get(user=self.user)
        except:
            u = None
        return u


class DownVotes(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Bookmark(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Thanks(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_sender_related")
    answerer = models.ForeignKey(User, on_delete=models.CASCADE,
                                 related_name="%(app_label)s_%(class)s_answerer_related")
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now=True)


class SuggestEdits(models.Model):
    suggester = models.ForeignKey(User, on_delete=models.CASCADE,
                                  related_name="%(app_label)s_%(class)s_suggester_related")
    original_writer = models.ForeignKey(User, on_delete=models.CASCADE,
                                        related_name="%(app_label)s_%(class)s_op_related")
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, null=True)
    created = models.DateTimeField(auto_now=True)


class AnonymousAnswerWriters(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
