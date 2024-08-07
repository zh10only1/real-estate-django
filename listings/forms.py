from django.forms import ModelForm
from .models import Listing

class ListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = '__all__'
        # fields = ['title', 'description', 'demo_link', 'source_link']
        exclude = ('is_published',)