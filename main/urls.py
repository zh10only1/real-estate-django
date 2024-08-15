from django.urls import path
from . import views
from pages.views import translate_all

app_name = 'main'

urlpatterns = [
    path('', views.home, name='home'),
    path('listing/', views.listings, name='listing'),
    path('blog/', views.blog, name='blog'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('profile/', views.agency_details, name='profile'),
    path('add-property/', views.add_property, name='add_property'),
    path('edit-property/<int:id>/', views.edit_property, name='edit_property'),
    path('delete-property/<int:id>/', views.delete_property, name='delete_property'),
    path('property-details/<int:id>/', views.single_details, name='property_details'),
    path('blog/single/', views.blog_single, name="blog_single"),
    path('send-email/', views.send_email, name='send_email'),
    path('faq/', views.faq, name='faq'),
    path('owner/', views.owner, name='owner'),
    path('real-estate-agent/', views.real_estate_agent, name='real-estate-agent'),\
    path('building-contractor/', views.building_contractor, name='building-contractor'),
    # temporary
    path('login-required/', views.loginRequired, name='login_required'),
    path('translate-all/', translate_all, name='translate'),
]