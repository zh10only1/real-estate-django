import email
from django.db import models
from datetime import datetime
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.

class Privacy(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    description = RichTextUploadingField(blank=True, null=True)
    is_published = models.BooleanField(default=True)
    created = models.DateTimeField(default=datetime.now, blank=True)

class Topbar(models.Model):
    phone = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    social_github = models.CharField(max_length=255, blank=True, null=True)
    social_facebook = models.CharField(max_length=255, blank=True, null=True)
    social_linkedin = models.CharField(max_length=255, blank=True, null=True)
    social_instagram = models.CharField(max_length=255, blank=True, null=True)
    social_twitter = models.CharField(max_length=255, blank=True, null=True)
    is_published = models.BooleanField(default=True)
    created = models.DateTimeField(default=datetime.now, blank=True)

class Article(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    description = RichTextUploadingField(blank=True, null=True)
    is_published = models.BooleanField(default=True)
    created = models.DateTimeField(default=datetime.now, blank=True)

    
class Translation(models.Model):
    PAGES = (
        ('home', 'home'),
        ('about', 'about'),
        ('listings', 'listings'),
        ('property details', 'property details'),
        ('blog', 'blog'),
        ('blog details', 'blog details'),
        ('contact', 'contact'),
        ('privacy', 'privacy'),
        ('navbar', 'navbar'),
        ('add-property', 'add-property'),
        ('profile', 'profile'),
        ('footer', 'footer'),
        ('login', 'login'),
        ('signup', 'signup'),
        ('faq', 'faq'),
        ('forget-password', 'forget-password'),
        ('reset-password', 'reset-password')
    )
    name = models.CharField(max_length=255, unique=True)
    page = models.CharField(max_length=50, choices=PAGES)
    english_content = models.TextField(blank=True)
    german_content = models.TextField(blank=True)
    french_content = models.TextField(blank=True)
    greek_content = models.TextField(blank=True)
    croatian_content = models.TextField(blank=True)
    polish_content = models.TextField(blank=True)
    czech_content = models.TextField(blank=True)
    russian_content = models.TextField(blank=True)
    swedish_content = models.TextField(blank=True)
    norway_content = models.TextField(blank=True)
    slovak_content = models.TextField(blank=True)
    dutch_content = models.TextField(blank=True)

    class Meta:
        ordering = ['name']