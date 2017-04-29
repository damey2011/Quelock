import datetime
from django.contrib.auth.models import User
from django.db import models

# upvotes to your answer
# new follower
# comment on your answer
# comment on your question # Yet to be implemented
# report notification
# new answer to followed question
# new answer by user you follow (if notification is turned on)
# new question under topic if notification is turned on
# new question under topic if notification is turned on
# new answers from people you requested answer from
# Suggested edits
# Gratification
import math
from django.utils.timezone import utc

from account.models import Reports, UserFollowings
from answers.models import UpVotes, Answer, SuggestEdits, Thanks
from comments.models import Comment
from messages.models import ConversationReplies
from questions.models import Question, AnswerRequest, QuestionFollowing


# FOR TURNED ON USER NOTIFICATIONS
class UserTurnedOnNotifications(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_user")
    subscriber = models.ForeignKey(User, on_delete=models.CASCADE,
                                   related_name="%(app_label)s_%(class)s_subscriber")
    created = models.DateTimeField(auto_now_add=True)


# FOR TURNED ON TOPIC NOTIFICATIONS
class TopicTurnedOnNotifications(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_topic")
    subscriber = models.ForeignKey(User, on_delete=models.CASCADE,
                                   related_name="%(app_label)s_%(class)s_subscriber")
    created = models.DateTimeField(auto_now_add=True)


notification_type = (
    (1, UpVotes),
    (2, ConversationReplies),
    (3, Answer),
    (4, Question),
    (5, Reports),
    (6, SuggestEdits),
    (7, Thanks),
    (8, Comment),
    (9, AnswerRequest),
    (10, UserTurnedOnNotifications),
    (11, TopicTurnedOnNotifications),
    (12, QuestionFollowing),
    (13, UserFollowings)
)


class Notification(models.Model):
    actor = models.ForeignKey(User, models.CASCADE, related_name='actor', null=True)
    owner = models.ForeignKey(User, models.CASCADE, related_name='owner')
    note_type = models.PositiveIntegerField(choices=notification_type)
    notification_id = models.PositiveIntegerField(default=1)
    time = models.DateTimeField(auto_now_add=True)
    read_status = models.BooleanField(default=False)

    @property
    def time_added(self):
        time_diff = datetime.datetime.now(utc) - self.time
        if time_diff.days < 1:
            if time_diff.seconds < 60:
                return str(math.floor(time_diff.seconds)) + 's'
            elif 60 <= time_diff.seconds < 3600:
                return str(math.floor(time_diff.seconds / 60)) + 'm'
            elif 3600 <= time_diff.seconds < 5184000:
                return str(math.floor(time_diff.seconds / 3600)) + 'h'
        elif 1 < time_diff.days < 30:
            return str(math.floor(time_diff.days)) + 'd'
        elif time_diff.days == 1:
            return 'Yesterday'
        else:
            return self.time.date()

    @property
    def get_note_answer_object(self):
        a = Answer.objects.get(pk=self.notification_id)
        print(a)
        return a

    @property
    def get_note_thanks_object(self):
        return Thanks.objects.get(pk=self.notification_id)

    @property
    def get_note_comment_object(self):
        return Comment.objects.get(pk=self.notification_id)

    @property
    def get_note_answer_request_object(self):
        return AnswerRequest.objects.get(pk=self.notification_id)

    @property
    def get_note_user_following_object(self):
        return UserFollowings.objects.get(pk=self.notification_id)

    def get_html_equivalent(self):
        if self.note_type == 1:
            return "%s %s upvoted your answer" % (self.actor.first_name, self.actor.last_name)
        if self.note_type == 2:
            return "%s %s sent you a message" % (self.actor.first_name, self.actor.last_name)
        if self.note_type == 3:
            pass
        if self.note_type == 4:
            pass
        if self.note_type == 5:
            pass
        if self.note_type == 6:
            pass
        if self.note_type == 7:
            return "%s %s thanked you for your answer to <b>%s</b>" % (
                self.actor.first_name, self.actor.last_name, self.get_note_thanks_object.answer.question.title)
        if self.note_type == 8:
            parent_answer = self.get_note_comment_object.parent_answer
            if parent_answer:
                return "%s %s commented on your answer" % (self.actor.first_name, self.actor.last_name)
            else:
                return "%s %s replied to your comment"
        if self.note_type == 9:
            return "%s %s requested your answer to <b>%s</b>" % (
                self.actor.first_name, self.actor.last_name, self.get_note_answer_request_object.question.title)
        if self.note_type == 10:
            pass
        if self.note_type == 11:
            pass
        if self.note_type == 12:
            pass
        if self.note_type == 13:
            return "%s %s started following you" % (self.actor.first_name, self.actor.last_name)

    def get_notification_link(self):
        pass
