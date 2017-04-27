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
