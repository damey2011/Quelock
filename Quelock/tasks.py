import datetime
from django.contrib.auth.models import User
from django.utils.timezone import utc
from Quelock.celery import app
from account.models import Reports, AlreadyReadAnswers, UserFigures, UserFollowings
from answers.models import UpVotes, Answer, SuggestEdits, Thanks
from comments.models import Comment
from messages.models import ConversationReplies
from notifications.serializers import NotificationSerializer
from notifications.models import Notification, UserTurnedOnNotifications
from questions.models import AnswerRequest, QuestionFollowing, Question, ReadQuestions


@app.task(bind=True, default_retry_delay=30 * 60)
def upvote_notify(self, answer_id, actor):
    answer_id = int(answer_id)
    try:
        a = Answer.objects.get(pk=answer_id)
        owner = a.writer.user
        n = Notification(actor_id=actor, owner=owner, note_type=1, notification_id=answer_id)
        n.save()

        a.no_of_upvotes += 1
        a.save()

        uf = UserFigures.objects.get(user=owner)
        uf.upvotes += 1
        uf.save()
        return NotificationSerializer(n).data
    except Exception as e:
        self.retry(exc=e, countdown=60)


@app.task(bind=True, default_retry_delay=30 * 60)
def decr_no_of_upvotes(self, answer_id):
    try:
        a = Answer.objects.get(pk=answer_id)
        a.no_of_upvotes -= 1
        a.save()

        uf = UserFigures.objects.get(user=a.writer.user)
        uf.upvotes += 1
        uf.save()
        return {'answer': answer_id, 'action': 'decr_upvotes', 'no_of_upvotes': a.no_of_upvotes}
    except Exception as e:
        self.retry(exc=e, countdown=60)


@app.task(bind=True, default_retry_delay=30 * 60)
def addAnswerView(self, user_id, answer_id):
    # The answer view can only be incremented once in 24 hours
    user_id = int(user_id)
    answer_id = int(answer_id)
    a = Answer.objects.get(pk=answer_id)
    try:
        # Add the answer to the list of already read answers by user
        ara = AlreadyReadAnswers.objects.filter(user_id=user_id, answer_id=answer_id)
        count = ara.count()
        if count > 0:
            last_viewd = count - 1
            time_diff = datetime.datetime.now(utc) - ara[last_viewd].created

            if time_diff.days >= 1:
                AlreadyReadAnswers(user_id=user_id, answer_id=answer_id).save()
                a.no_of_views += 1
                a.save()
                incr_user_total_views(a.writer.user.id)
        else:
            AlreadyReadAnswers(user_id=user_id, answer_id=answer_id).save()
            a.no_of_views += 1
            a.save()
            incr_user_total_views(a.writer.user.id)
        return {'answer_id': answer_id, 'action': 'view+1'}
    except Exception as e:
        self.retry(exc=e, countdown=60)


@app.task(bind=True, default_retry_delay=30 * 60)
def add_comment_count(self, answer_id, user_id):
    try:
        pass
    except Exception as e:
        self.retry(exc=e, countdown=60)


@app.task(bind=True, default_retry_delay=30 * 60)
def message_notify(self, sender_id, conv_rep_id):
    cr = ConversationReplies.objects.get(pk=conv_rep_id)
    user_1 = cr.conv.user_1_id
    user_2 = cr.conv.user_2_id

    try:
        if user_1 == sender_id:
            Notification(actor_id=sender_id, owner_id=user_2, note_type=2, notification_id=conv_rep_id).save()
        else:
            Notification(actor_id=sender_id, owner_id=user_1, note_type=2, notification_id=conv_rep_id).save()
    except Exception as e:
        self.retry(exc=e, countdown=60)


# FOLLOW QUESTION
@app.task(bind=True, default_retry_delay=30 * 60)
def follow_question(self, question_id, user_id):
    try:
        QuestionFollowing(question_id=question_id, user_id=user_id).save()
    except Exception as e:
        self.retry(exc=e, countdown=60)


@app.task(bind=True, default_retry_delay=30 * 60)
def answer_written_notify(self, answer_id):
    try:
        # For the question asker
        a = Answer.objects.get(pk=answer_id)

        # For users following the question
        question = a.question
        qf = QuestionFollowing.objects.filter(question=question)

        for user in qf:
            n = Notification(actor_id=a.writer.id, owner_id=user.user.id, note_type=12, notification_id=answer_id)
            n.save()

        # For users who turned on notifications to the writer
        notification_subscribed_users = UserTurnedOnNotifications.objects.filter(user=a.writer.user).values(
            'subscriber').select_related()
        for user in notification_subscribed_users:
            n = Notification(actor_id=a.writer.id, owner_id=user.user.id, note_type=2, notification_id=answer_id)

    except Exception as e:
        self.retry(exc=e, countdown=60)


@app.task(bind=True, default_retry_delay=30 * 60)
def answer_requested_create_and_notify(self, requester, question, receipient):
    try:
        ar = AnswerRequest(requester_id=requester, receipient_id=receipient, question_id=question)
        ar.save()
        Notification(actor_id=requester, owner_id=receipient, note_type=9, notification_id=ar.id).save()
    except Exception as e:
        self.retry(exc=e, countdown=60)


@app.task(bind=True, default_retry_delay=30 * 60)
def thanks_create_and_notify(self, answer_id, user_id):
    try:
        answer = Answer.objects.get(pk=answer_id)
        t = Thanks(user_id=user_id, answerer=answer.writer.user, answer=answer)
        t.save()
        n = Notification(actor_id=user_id, owner_id=answer.writer.user.id, note_type=7, notification_id=t.id)
        n.save()
        return NotificationSerializer(n).data
    except Exception as e:
        self.retry(exc=e, countdown=60)


@app.task(bind=True, default_retry_delay=30 * 60)
def comment_notify(self, comment_id, type, parent_id):
    try:
        c = Comment.objects.get(pk=comment_id)
        if type == 1:
            p = Answer.objects.get(pk=parent_id)
            owner_id = p.writer.user.id

            uf = UserFigures.objects.get(user_id=c.writer.id)
            uf.comments += 1
            uf.save()
        else:
            p = Comment.objects.get(pk=parent_id)
            owner_id = p.writer.id

            uf = UserFigures.objects.get(user_id=c.writer.id)
            uf.comments += 1
            uf.save()

        n = Notification(actor_id=c.writer.id, owner_id=owner_id, note_type=8, notification_id=parent_id)
        n.save()
        return NotificationSerializer(n).data
    except Exception as e:
        self.retry(exc=e, countdown=60)


@app.task(bind=True, default_retry_delay=30 * 60)
def edit_suggested_notify(self, answer_id, user_id):
    try:
        pass
    except Exception as e:
        self.retry(exc=e, countdown=60)


@app.task(bind=True, default_retry_delay=30 * 60)
def addQuestionView(self, question_id, user_id):
    # The answer view can only be incremented once in 24 hours
    user_id = int(user_id)
    question_id = int(question_id)
    q = Question.objects.get(pk=question_id)
    try:
        # Add the answer to the list of already read answers by user
        rq = ReadQuestions.objects.filter(user_id=user_id, question_id=question_id)
        count = rq.count()
        if count > 0:
            last_viewd = count - 1
            time_diff = datetime.datetime.now(utc) - rq[last_viewd].created

            if time_diff.days >= 1:
                ReadQuestions(user_id=user_id, question_id=question_id).save()
                q.no_of_views += 1
                q.save()
        else:
            ReadQuestions(user_id=user_id, question_id=question_id).save()
            q.no_of_views += 1
            q.save()
        return {'question_id': question_id, 'action': 'view+1'}
    except Exception as e:
        self.retry(exc=e, countdown=60)


@app.task(bind=True, default_retry_delay=30 * 60)
def notify_of_new_follower(self, user_following_id):
    try:
        uf = UserFollowings.objects.get(pk=user_following_id)
        n = Notification(actor_id=uf.user_id, owner_id=uf.is_following_id, note_type=13,
                         notification_id=user_following_id)
        n.save()
    except Exception as e:
        self.retry(exc=e, countdown=60)


# OTHER SECONDARY METHODS
def incr_user_total_views(user_id):
    u = User.objects.get(pk=user_id).profile
    u.answer_no_of_views += 1
    u.save()
