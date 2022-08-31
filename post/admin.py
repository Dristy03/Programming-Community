from django.contrib import admin

from post.models import Comment, Post, Notification


# Registers Post models for admin panel
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Notification)
