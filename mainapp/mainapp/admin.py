from django.contrib import admin
from mainapp.models import Post,Comment,PostTag

admin.site.register(Comment)
admin.site.register(Post)
admin.site.register(PostTag)
