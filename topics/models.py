from django.contrib.auth.models import User
from django.db import models
from django.db.models.functions import datetime
from django.utils.text import slugify


class Topic(models.Model):
    title = models.CharField(max_length=100)
    desc = models.TextField(blank=True)
    image_name = models.ImageField(null=True, blank=True, upload_to='topics-dp')
    no_following_topic = models.IntegerField(null=True, default=0, blank=True)
    no_of_questions_under_topic = models.IntegerField(null=True, default=0, blank=True)
    slug = models.SlugField(max_length=100, unique=True, null=True, blank=True)
    created = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(User, blank=True, null=True)

    def __str__(self):
        return self.title

    def image_url(self):
        return self.image_name.url

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Topic, self).save(*args, **kwargs)


class TopicFollowing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    follows = models.ForeignKey(Topic, on_delete=models.CASCADE)
    created = models.DateTimeField(null=True)

    def __str__(self):
        return self.user.user.first_name + ' FOLLOWS ' + self.follows.title

    def save(self, *args, **kwargs):
        if not self.created:
            self.created = datetime.timezone.now()
        super(TopicFollowing, self).save(*args, **kwargs)
