from django.contrib import admin
from answers.models import Answer, UpVotes, DownVotes

admin.site.register(Answer)
admin.site.register(UpVotes)
admin.site.register(DownVotes)
