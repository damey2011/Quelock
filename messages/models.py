import datetime
from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import utc
import math


class Conversation(models.Model):
    user_1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_1')
    user_2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_2')
    time = models.DateTimeField(auto_now_add=True)


class ConversationReplies(models.Model):
    conv = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    reply = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    read_status = models.BooleanField(default=False)

    @property
    def period_sent(self):
        time_diff = datetime.datetime.now(utc) - self.time
        print(time_diff)
        print(time_diff.days)
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
            return self.time.date()
