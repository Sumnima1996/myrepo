from django.contrib import admin

# Register your models here.
from .models import Question,Answer,Tag

admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Tag)