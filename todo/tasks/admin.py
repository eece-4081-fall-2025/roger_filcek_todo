from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "completed", "archived", "created_at", "updated_at")
    list_filter = ("completed", "archived")
    search_fields = ("title", "details")
