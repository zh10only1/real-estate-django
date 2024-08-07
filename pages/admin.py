from django.contrib import admin

# Register your models here.

from .models import Privacy, Topbar, Article, Translation


class PrivacyAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'is_published', 'created')
    list_display_links = ('id', 'title')
    list_editable = ('is_published',)
    search_fields = ('title',)
    list_per_page = 25

admin.site.register(Privacy, PrivacyAdmin)

class TopbarAdmin(admin.ModelAdmin):
    list_display = ('id', 'phone', 'email' , 'created')
    list_display_links = ('id', 'phone')
    search_fields = ('phone',)
    list_per_page = 25

admin.site.register(Topbar, TopbarAdmin)


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_published', 'created')
    list_display_links = ('id', 'name')
    list_editable = ('is_published',)
    search_fields = ('name',)
    list_per_page = 25

admin.site.register(Article, ArticleAdmin)

class TranslationAdmin(admin.ModelAdmin):
    list_display = ('name', 'page','short_english_content')
    list_display_links = ('name', 'page')
    search_fields = ('name', 'page')
    list_filter = ('page',)

    def short_english_content(self, obj):
        return f"{obj.english_content[:50]}..." if len(obj.english_content) > 50 else obj.english_content

admin.site.register(Translation, TranslationAdmin)