from django.contrib import admin

from posts.models import Post, Follow, ReadPost

admin.site.register(Post)
admin.site.register(ReadPost)
admin.site.register(Follow)
