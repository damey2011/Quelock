from django.contrib import admin
from messages.models import Conversation, ConversationReplies

admin.site.register(Conversation)
admin.site.register(ConversationReplies)
