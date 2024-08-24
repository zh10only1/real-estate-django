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
    path('blog-single-1', views.blog_single_1, name="blog-single-1"),
    path('blog-single-2', views.blog_single_2, name="blog-single-2"),
    path('blog-single-3', views.blog_single_3, name="blog-single-3"),
    path('send-email/', views.send_email, name='send_email'),
    path('send-registration-email/', views.send_registration_email, name='send-registration-email'),
    path('send-owner-form/', views.send_owner_form, name='send-owner-form'),
    path('faq/', views.faq, name='faq'),
    path('owner/', views.owner, name='owner'),
    path('real-estate-agent/', views.real_estate_agent, name='real-estate-agent'),\
    path('building-contractor/', views.building_contractor, name='building-contractor'),
    path('realestate-contractor-registration', views.realestate_contractor_registration, name='realestate-contractor-registration'),
    path('owner-form/', views.owner_form, name='owner-form'),
    path('imprint/', views.imprint, name='imprint'),
    path('data-protection/', views.data_protection, name='data-protection'),
    path('agb', views.agb, name='agb'),
    path('cancellation-policy', views.cancellation_policy, name='cancellation-policy'),
    path('sitemap', views.sitemap, name='sitemap'),
    path('service', views.service, name='service'),
    # temporary
    path('login-required/', views.loginRequired, name='login_required'),
    path('translate-all/', translate_all, name='translate'),
    
]