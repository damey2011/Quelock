import datetime
from django.contrib.auth.models import User
from django.db import models
import math
from django.utils.timezone import utc
from account.models import UserOtherDetails, AlreadyReadAnswers
from comments.models import Comment
from questions.models import Question
from topics.models import Topic


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True)
    writer = models.ForeignKey(UserOtherDetails, on_delete=models.SET('Anonymous'))
    time_written = models.DateTimeField(auto_now_add=True)
    body = models.TextField()
    no_of_upvotes = models.IntegerField(null=True, default=0)
    no_of_downvotes = models.IntegerField(null=True, default=0)
    no_of_views = models.IntegerField(null=True, default=0)
    no_of_comments = models.IntegerField(null=True, default=0)
    edited = models.IntegerField(null=True, default=0)
    anonymous = models.BooleanField(default=False)
    total_activities = models.IntegerField(default=0)

    def __str__(self):
        return self.question.title

    def upvotesCount(self):
        try:
            return UpVotes.objects.filter(answer=self).count()
        except Exception as e:
            print(e)

    def answerViews(self):
        try:
            return AlreadyReadAnswers.objects.filter(answer=self).count()
        except:
            return 0

    def getComments(self):
        try:
            return Comment.objects.filter(parent_answer=self).count()
        except Exception as e:
            return 0

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

    @property
    def time_answered(self):
        time_diff = datetime.datetime.now(utc) - self.time_written
        if time_diff.days < 1:
            if time_diff.seconds < 60:
                return str(math.floor(time_diff.seconds)) + 's'
            elif 60 <= time_diff.seconds < 3600:
                return str(math.floor(time_diff.seconds/60)) + 'm'
            elif 3600 <= time_diff.seconds < 5184000:
                return str(math.floor(time_diff.seconds/3600)) + 'h'
        elif 1 < time_diff.days < 30:
            return str(math.floor(time_diff.days)) + 'd'
        elif time_diff.days == 1:
            return 'Yesterday'
        else:
            return self.time_written.date()

    def save(self, *args, **kwargs):
        self.total_activities = int(self.no_of_upvotes) + int(self.no_of_comments)
        return super(Answer, self).save(*args, **kwargs)


class UpVotes(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)

    def get_user_details(self):
        try:
            u = UserOtherDetails.objects.get(user=self.user)
        except:
            u = None
        return u


class DownVotes(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)


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
