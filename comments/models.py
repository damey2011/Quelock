from django.contrib.auth.models import User
from django.db import models
from account.models import UserOtherDetails


class Comment(models.Model):
    writer = models.ForeignKey(User, on_delete=models.SET('Anonymous'), null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    body = models.TextField()
    no_of_upvotes = models.IntegerField(null=True, default=0)
    edited = models.IntegerField(null=True, default=0)
    parent = models.ForeignKey("self", null=True, blank=True)
    parent_answer = models.ForeignKey("answers.Answer", related_name='comment_ans', null=True, blank=True)

    class Meta:
        ordering = ['-timestamp']

    def children(self):
        return Comment.objects.filter(parent=self)

    def children_count(self):
        return Comment.objects.filter(parent=self).count()

    @property
    def is_parent(self):
        if self.parent is not None:
            return False
        return True
