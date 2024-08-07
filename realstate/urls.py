from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static 
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _
from main.views import set_language_from_url

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path("set-language/<str:user_language>/", set_language_from_url, name="set_language_from_url"),
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    # path('', include('pages.urls')),
    # path('', include('realtors.urls')),
    # path('listings/', include('listings.urls')),   ### listings need to add before apps urls
    path('accounts/', include('accounts.urls')),   ### accounts need to add before apps urls
    # path('contacts/', include('contacts.urls')),
    path('', include('main.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)       ## Media Folder

