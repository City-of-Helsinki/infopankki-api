from django.contrib import admin
from .models import MasterPage


class MasterPageAdmin(admin.ModelAdmin):
    pass
admin.site.register(MasterPage, MasterPageAdmin)
