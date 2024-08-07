from django.contrib import admin

from .models import Realtor, Interface


class RealtorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'is_mvp', 'hire_date')
    list_display_links = ('id', 'name')
    list_filter = ('name',)
    list_editable = ('is_mvp',)
    search_fields = ('name',)
    list_per_page = 25


# Register your models here.
#admin.site.register(Realtor, RealtorAdmin)

class InterfaceAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'is_published', 'created')
    list_display_links = ('id', 'title')
    list_filter = ('title',)
    list_editable = ('is_published',)
    search_fields = ('title',)
    list_per_page = 25


# Register your models here.
#admin.site.register(Interface, InterfaceAdmin)