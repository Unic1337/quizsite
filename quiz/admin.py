from django.contrib import admin
from .models import Quiz, QuizResult


class QuizAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')


admin.site.register(Quiz, QuizAdmin)
admin.site.register(QuizResult)
