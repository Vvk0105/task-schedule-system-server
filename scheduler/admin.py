from django.contrib import admin
from .models import Task, TaskExecutionHistory

# Register your models here.

admin.site.register(Task)
admin.site.register(TaskExecutionHistory)