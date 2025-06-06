from django.contrib import admin
from .models import Trivia

class TriviaAdmin(admin.ModelAdmin):
    ordering = ['name']
    search_fields = ['name']

admin.site.register(Trivia, TriviaAdmin)