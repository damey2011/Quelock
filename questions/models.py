from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.datetime_safe import datetime
from django.utils.text import slugify
from topics.models import Topic


class Question(models.Model):
    title = models.CharField(max_length=150)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    question_details = models.TextField(blank=True)
    no_following_quest = models.IntegerField(blank=True, default=0)
    no_of_answers = models.IntegerField(blank=True, default=0)
    no_of_views = models.IntegerField(blank=True, default=0)
    date_asked = models.DateField(null=True)
    time_asked = models.TimeField(null=True)
    slug = models.SlugField(max_length=100, unique=True, null=True)
    anonymous = models.BooleanField(default=False)

    class Meta:
        ordering = ["-date_asked", "-time_asked"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Question, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('q_detail', kwargs={"slug": self.slug})


class QuestionTopic(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    under = models.ForeignKey(Topic, on_delete=models.CASCADE)

    def __str__(self):
        return self.question.title + ' CATEGORIZED UNDER ' + self.under.title


class QuestionImageUpload(models.Model):
    image = models.ImageField(upload_to='question-images/%Y/%m/%d')

    # def save(self, *args, **kwargs):
    #     super(QuestionImageUpload, self).save(*args, **kwargs)
    #     return self.image


class QuestionFollowing(models.Model):
    user = models.ForeignKey("account.UserOtherDetails", on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    created = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.created:
            self.created = datetime.now()
        super(QuestionFollowing, self).save(*args, **kwargs)


class AnonymousQuestionsWriters(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class ReadQuestions(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now=True)
