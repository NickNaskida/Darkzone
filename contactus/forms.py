from django import forms
from django.forms.widgets import TextInput

from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox

class ContactForm(forms.Form):
	name = forms.CharField(required=True, widget=TextInput(attrs={'placeholder': 'Name'})) #subject
	email = forms.EmailField(required=True, label='Your Email', widget=TextInput(attrs={'placeholder': 'Your Email'})) #from email
	message = forms.CharField(widget=forms.Textarea) #message
	captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox(attrs={'data-theme': 'dark'}), label='')
