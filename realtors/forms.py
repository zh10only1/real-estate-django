from django.forms import ModelForm
from .models import Interface

class InterfaceForm(ModelForm):
    class Meta:
        model = Interface
        fields = '__all__'
        # fields = ['title', 'description', 'demo_link', 'source_link']
        exclude = ('is_published',)