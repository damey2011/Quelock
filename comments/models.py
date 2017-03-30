from django.db import models
from account.models import UserOtherDetails


class CommentManager(models.Manager):
    def all(self):
        qs = super(CommentManager, self).filter(parent=None)
        return qs


class Comment(models.Model):
    writer = models.ForeignKey(UserOtherDetails, on_delete=models.SET('Anonymous'), null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    body = models.TextField()
    no_of_upvotes = models.IntegerField(null=True, default=0)
    edited = models.IntegerField(null=True, default=0)
    parent = models.ForeignKey("self", null=True, blank=True)
    parent_answer = models.ForeignKey("answers.Answer", related_name='comment_ans', null=True, blank=True)

    objects = CommentManager()

    def __str__(self):
        return self.question.title

    class Meta:
        ordering = ['-timestamp']

    def children(self):
        return Comment.objects.filter(parent=self)

    @property
    def is_parent(self):
        if self.parent is not None:
            return False
        return True
