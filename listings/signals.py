from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from .models import Listing
from .translate import detect_language, translate_object
import threading
import json
import time
from translate import Translator


def translate_listing(id, obj):
    listing = Listing.objects.get(id=id)
    language = detect_language(obj).strip()
    all_languages = ["English", "German", "French", "Greek", "Croatian", "Polish", "Czech", "Russian", "Swedish", "Norway", "Slovak", "Dutch"]
    if language == "English": listing.english_content = json.dumps(obj)
    if language == "German": listing.german_content = json.dumps(obj)
    if language == "French": listing.french_content = json.dumps(obj)
    if language == "Greek": listing.greek_content = json.dumps(obj)
    if language == "Croatian": listing.croatian_content = json.dumps(obj)
    if language == "Polish": listing.polish_content = json.dumps(obj)
    if language == "Czech": listing.czech_content = json.dumps(obj)
    if language == "Russian": listing.russian_content = json.dumps(obj)
    if language == "Swedish": listing.swedish_content = json.dumps(obj)
    if language == "Norway": listing.norway_content = json.dumps(obj)
    if language == "Slovak": listing.slovak_content = json.dumps(obj)
    if language == "Dutch": listing.dutch_content = json.dumps(obj)
    listing.save()
    
    if language in all_languages: all_languages.remove(language)
    for lang in all_languages:
        translated_obj = translate_object(obj, language, lang)
        if not translated_obj: continue
        if lang == "English": listing.english_content = json.dumps(translated_obj)
        if lang == "German": listing.german_content = json.dumps(translated_obj)
        if lang == "French": listing.french_content = json.dumps(translated_obj)
        if lang == "Greek": listing.greek_content = json.dumps(translated_obj)
        if lang == "Croatian": listing.croatian_content = json.dumps(translated_obj)
        if lang == "Polish": listing.polish_content = json.dumps(translated_obj)
        if lang == "Czech": listing.czech_content = json.dumps(translated_obj)
        if lang == "Russian": listing.russian_content = json.dumps(translated_obj)
        if lang == "Swedish": listing.swedish_content = json.dumps(translated_obj)
        if lang == "Norway": listing.norway_content = json.dumps(translated_obj)
        if lang == "Slovak": listing.slovak_content = json.dumps(translated_obj)
        if lang == "Dutch": listing.dutch_content = json.dumps(translated_obj)
        listing.save()
        time.sleep(20)



@receiver(post_save, sender=Listing)
def post_save_listing(sender, instance, created, **kwargs):
    if not created: return
    my_obj = {
        "oib_number": instance.oib_number,
        "property_title": instance.property_title,
        "property_description": instance.property_description,
        "property_type": instance.property_type,
        "property_status": instance.property_status,
        "location": instance.location,
        "bedrooms": instance.bedrooms,
        "bathrooms": instance.bathrooms,
        "floors": instance.floors,
        "garage": instance.garage,
        "area": instance.area,
        "size": float(instance.size),
        "property_price": instance.property_price,
        "address": instance.address,
        "country": instance.country,
        "city": instance.city,
        "state": instance.state,
        "zipcode": instance.zipcode,
        "neighborhood": instance.neighborhood,
    }

    threading.Timer(1.0, translate_listing, args=[instance.id, my_obj]).start()
    