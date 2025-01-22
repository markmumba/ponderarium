from django.contrib import admin
from .models import User, Source, Theme, Quote, Comment, Upvote

admin.site.register(User)
admin.site.register(Source)
admin.site.register(Theme)
admin.site.register(Quote)
admin.site.register(Comment)
admin.site.register(Upvote)
