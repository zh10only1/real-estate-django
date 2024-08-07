from django.db import models
from django.contrib.auth.models import User
import uuid
# Create your models here.

class Agent(models.Model):
    GENDERS = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=200, blank=True, null=True)
    last_name = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(max_length=500, blank=True, null=True)
    gender = models.CharField(max_length=200, choices=GENDERS, blank=True, null=True)
    city = models.CharField(max_length=200, blank=True, null=True)
    country = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(upload_to='agents/', blank=True, null=True)
    # company data, logo, portrait photo of the contact person, Croatian OIB number, email address, and domain
    company_name = models.CharField(max_length=200, blank=True, null=True)
    company_logo = models.ImageField(upload_to='company/', blank=True, null=True)
    portrait_photo = models.ImageField(upload_to='portrait/', blank=True, null=True)
    oib_number = models.CharField(max_length=200, blank=True, null=True)
    domain = models.CharField(max_length=200, blank=True, null=True)

    is_active = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return str(self.user.username)
    
    class Meta:
        verbose_name_plural = 'Agent'
        verbose_name = 'Agent'
        ordering = ['-created']

class OTPVerification(models.Model):
    """
    This is a table for storing OTP verification.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    sent_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username