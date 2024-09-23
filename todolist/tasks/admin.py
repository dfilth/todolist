from django.contrib import admin
from todolist.tasks.models import Task

# Register your models here.
admin.site.register(Task)
