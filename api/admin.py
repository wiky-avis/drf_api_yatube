from django.contrib import admin

from .models import Comment, Follow, Group, Post

# Register your models here.
admin.site.register(Post)
admin.site.register(Group)
admin.site.register(Comment)
admin.site.register(Follow)
