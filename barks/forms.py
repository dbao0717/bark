from django import forms
from .models import Bark
from django.conf import settings

MAX_BARK_LENGTH = settings.MAX_BARK_LENGTH

class BarkForm(forms.ModelForm):
    class Meta:
        model = Bark
        fields = ['content']
    
    def clean_content(self):
        content = self.cleaned_data.get("content")
        if len(content) > MAX_BARK_LENGTH:
            raise forms.ValidationError("This bark is too long. Please limit barks to 240 characters")
        return content