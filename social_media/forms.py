from django import forms
from .models import *

class InstagramProfileForm(forms.ModelForm):
    class Meta:
        model = InstagramProfile
        fields = '__all__'

    def clean_link(self):
        link = self.cleaned_data.get('link')
        if not link.startswith("https://www.instagram.com/") and not link.startswith("https://instagram.com/"):
            raise forms.ValidationError("Invalid Instagram link. It must start with 'https://www.instagram.com/' or 'https://instagram.com/'")
        return link

class FacebookProfileForm(forms.ModelForm):
    class Meta:
        model = FacebookProfile
        fields = '__all__'

    def clean_link(self):
        link = self.cleaned_data.get('link')
        if not link.startswith("https://www.facebook.com/") and not link.startswith("https://facebook.com/"):
            raise forms.ValidationError("Invalid Facebook link. It must start with 'https://www.facebook.com/' or 'https://facebook.com/'")
        return link

class WhatsappProfileForm(forms.ModelForm):   
    class Meta:
        model = WhatsappProfile
        fields = '__all__'

    def clean_link(self):
        link = self.cleaned_data.get('link')
        if not link.startswith("https://wa.me/"):
            raise forms.ValidationError("Invalid Whatsapp link. It must start with 'https://wa.me/'")
        return link

class TelegramProfileForm(forms.ModelForm):  
    class Meta:
        model = TelegramProfile
        fields = '__all__'

    def clean_link(self):
        link = self.cleaned_data.get('link')
        if not link.startswith("https://t.me/") and not link.startswith("https://telegram.me/"):
            raise forms.ValidationError("Invalid Telegram link. It must start with 'https://t.me/' or 'https://telegram.me/'")
        return link
    
class TiktokProfileForm(forms.ModelForm):
    class Meta:
        model = TiktokProfile
        fields = '__all__'

    def clean_link(self):
        link = self.cleaned_data.get('link')
        if not link.startswith("https://www.tiktok.com/") and not link.startswith("https://tiktok.com/"):
            raise forms.ValidationError("Invalid Tiktok link. It must start with 'https://www.tiktok.com/' or 'https://tiktok.com/'")
        return link
