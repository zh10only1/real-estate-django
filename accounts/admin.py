from django.contrib import admin
from .models import Agent


class AgentsAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'user', 'email', 'is_active', 'created')
    list_display_links = ('first_name', 'last_name', 'user')
    list_editable = ('is_active',)
    search_fields = ('user',)
    list_per_page = 25


# Register your models here.
admin.site.register(Agent, AgentsAdmin)