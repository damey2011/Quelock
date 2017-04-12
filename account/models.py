from django.contrib.auth.models import User, AbstractUser
from django.db import models
from questions.models import Question
from topics.models import Topic
import math


def shorten_number(n):
    m = n
    length = len(str(n))
    if 3 < length < 7:
        n /= 1000
        mod = math.fmod(m, 1000)
        if mod == 0 or mod < 50:
            return str(math.floor(n)) + 'k'
        else:
            return str(round(n, 1)) + 'k'

    if 6 < length < 10:
        n /= 1000000
        mod = math.fmod(m, 1000000)
        if mod == 0 or mod < 50000:
            return str(math.floor(n)) + 'm'
        else:
            return str(round(n, 1)) + 'm'

    if 9 < length < 13:
        n /= 1000000000
        mod = math.fmod(m, 1000000000)
        if mod == 1 or mod < 50000000:
            return str(math.floor(n)) + 'b'
        else:
            return str(round(n, 1)) + 'b'

    else:
        return n


class UserOtherDetails(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    profile_no_of_views = models.IntegerField(null=True, default=0)
    display_picture = models.ImageField(null=True, blank=True, upload_to='dps', default='/default/user.png')
    bio = models.TextField(null=True, blank=True, default='NA')
    college = models.CharField(max_length=50, blank=True, default='NA')
    works = models.CharField(max_length=100, blank=True, default='NA')
    lives = models.CharField(max_length=50, blank=True, default='NA')
    followers = models.IntegerField(default=0)
    following = models.IntegerField(default=0)
    most_active_topic = models.ForeignKey(Topic, models.CASCADE, blank=True, null=True)
    facebook_link = models.URLField(max_length=100, blank=True, default='http://facebook.com')
    twitter_link = models.URLField(max_length=100, blank=True, default='http://twitter.com')
    linked_in_profile = models.URLField(max_length=100, blank=True, default='http://linkedin.com')
    no_of_questions = models.IntegerField(default=0)
    no_of_answers = models.IntegerField(default=0)

    User.profile = property(lambda u: UserOtherDetails.objects.get_or_create(user=u)[0])

    def __str__(self):
        return self.user.username

    def set_dp_image(self, url):
        new_url = str(url).split('/')
        last_string = '/media/dps/' + new_url[len(new_url) - 1]
        return last_string

    def get_no_of_followers(self):
        user = UserOtherDetails.objects.get(user=self.user)
        u = UserFollowings.objects.filter(is_following=user).count()
        return shorten_number(u)

    def get_no_of_following(self):
        user = UserOtherDetails.objects.get(user=self.user)
        u = UserFollowings.objects.filter(user=user).count()
        return shorten_number(u)

    def get_no_of_questions(self):
        return Question.objects.filter(author=self.user).count()

    def increase_no_of_answers(self):
        self.no_of_answers += 1

    def get_dp_url(self):
        return self.display_picture.url


class UserFollowings(models.Model):
    user = models.ForeignKey(UserOtherDetails, related_name='%(app_label)s_%(class)s_related', on_delete=models.CASCADE)
    is_following = models.ForeignKey(UserOtherDetails, related_name='%(app_label)s_%(class)s', on_delete=models.CASCADE)
    created = models.DateTimeField(null=True)

    def follows(self, user, flwrsOrflwngs):
        if flwrsOrflwngs == 1:
            flwrsOrflwngs = self.is_following
        else:
            flwrsOrflwngs = self.user
        user = UserOtherDetails.objects.get(user=user)
        try:
            user_following = UserFollowings.objects.get(user=user, is_following=flwrsOrflwngs)
        except:
            user_following = None
        if user_following is not None:
            return True
        else:
            return False


class AlreadyReadAnswers(models.Model):
    user = models.ForeignKey(User, related_name='%(app_label)s_%(class)s_related', on_delete=models.CASCADE)
    answer = models.ForeignKey("answers.Answer", related_name='%(app_label)s_%(class)s_related',
                               on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)


TYPES = (
    ('A', 'Answer'),
    ('Q', 'Question'),
    ('U', 'User')
)


class Reports(models.Model):
    type = models.CharField(max_length=1, choices=TYPES)
    type_id = models.PositiveIntegerField()
    created = models.DateTimeField(auto_now_add=True,null=True)
    message = models.TextField(blank=True, null=True)


class UserNotifications(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_user")
    subscriber = models.ForeignKey(User, on_delete=models.CASCADE,
                                   related_name="%(app_label)s_%(class)s_subscriber")
