from django.template.defaulttags import register
from answers.models import UpVotes, DownVotes, Thanks, SuggestEdits, Bookmark
from questions.models import QuestionTopic


@register.assignment_tag(name="isupvoted", takes_context=True)
def isupvoted(context, *args, **kwargs):
    return UpVotes.objects.filter(user=context['request'].user, answer=context['answer']).exists()


@register.simple_tag(name="isdownvoted", takes_context=True)
def isdownvoted(context, *args, **kwargs):
    return DownVotes.objects.filter(user=context['request'].user, answer=context['answer']).exists()


@register.simple_tag(name="isthanked", takes_context=True)
def isthanked(context, *args, **kwargs):
    return Thanks.objects.filter(user=context['request'].user, answer=context['answer']).exists()


@register.simple_tag(name="editsuggested", takes_context=True)
def editsuggested(context, *args, **kwargs):
    return SuggestEdits.objects.filter(suggester=context['request'].user, answer=context['answer']).exists()


@register.simple_tag(name="bookmarked", takes_context=True)
def bookmarked(context, *args, **kwargs):
    return Bookmark.objects.filter(user=context['request'].user, answer=context['answer']).exists()


@register.assignment_tag(name="topic_tags", takes_context=True)
def topic_tags(context, *args, **kwargs):
    print(context['answer'].question)
    return QuestionTopic.objects.filter(question=context['answer'].question)
