from django.contrib import admin

# Register your models here.

from .models import Blog, Topic, Message, User

admin.site.register(User)
admin.site.register(Blog)
admin.site.register(Topic)
admin.site.register(Message)
