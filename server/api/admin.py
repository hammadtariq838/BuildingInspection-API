from django.contrib import admin
from .models import Project, Asset, Action, Method

# Register your models here.
admin.site.register(Project)
admin.site.register(Asset)
admin.site.register(Method)
admin.site.register(Action)