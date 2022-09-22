from django.contrib import admin
from .models import News, Comment, Status, NewsStatus, CommentStatus

admin.site.register(News)
admin.site.register(Comment)
admin.site.register(Status)
admin.site.register(NewsStatus)
admin.site.register(CommentStatus)
