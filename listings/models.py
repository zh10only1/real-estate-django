from django.db import models
from datetime import datetime
from accounts.models import Agent
import json
# Create your models here.

class Listing(models.Model):
    company_name = models.CharField(max_length=200, blank=True, null=True)
    company_logo = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True, null=True)
    portrait_photo = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True, null=True)
    oib_number = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(max_length=500, blank=True, null=True)
    domain = models.CharField(max_length=200, blank=True, null=True)
    realtor = models.ForeignKey(Agent, on_delete=models.DO_NOTHING, blank=True, null=True)
    property_title = models.CharField(max_length=200, blank=True)
    property_description = models.TextField(blank=True)
    property_type = models.CharField(max_length=200, blank=True)
    property_status = models.CharField(max_length=200, blank=True)
    location = models.CharField(max_length=200, blank=True)
    bedrooms = models.IntegerField(blank=True)
    bathrooms = models.IntegerField(default=0, blank=True)
    floors = models.IntegerField()
    garage = models.IntegerField(default=0)
    area = models.IntegerField()
    size = models.DecimalField(max_digits=5, decimal_places=1)
    property_price = models.IntegerField(default=0, blank=True)
    property_id = models.IntegerField(default="1", blank=True)
    video_url = models.CharField(max_length=200, blank=True)
    photo_main = models.ImageField(upload_to='photos/%Y/%m/%d/')
    photo_1 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)   ## blank=True used to make this field optional
    photo_2 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_3 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_4 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_5 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_6 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    is_published = models.BooleanField(default=True)
    list_date = models.DateTimeField(default=datetime.now, blank=True)
    address = models.CharField(max_length=200, blank=True)
    country = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    zipcode = models.CharField(max_length=20, blank=True)
    neighborhood = models.CharField(max_length=100, blank=True)

    #translate
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
    
    def __str__(self):
        return self.property_title
    
    def get_json(self):
        return {
            "oib_number": self.oib_number,
            "property_title": self.property_title,
            "property_description": self.property_description,
            "property_type": self.property_type,
            "property_status": self.property_status,
            "location": self.location,
            "bedrooms": self.bedrooms,
            "bathrooms": float(self.bathrooms),
            "floors": self.floors,
            "garage": self.garage,
            "area": self.area,
            "size": float(self.size),
            "property_price": self.property_price,
            "address": self.address,
            "country": self.country,
            "city": self.city,
            "state": self.state,
            "zipcode": self.zipcode,
            "neighborhood": self.neighborhood,
        }
