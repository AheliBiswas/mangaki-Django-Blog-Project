from django.contrib import admin
from blogs.models import Blog,Tag,Comment
# Register your models here.

admin.site.register(Blog)
admin.site.register(Tag)
admin.site.register(Comment)