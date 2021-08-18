from django import forms

from datetime import datetime

from users.models import UserProfile 
		
class ProfileForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.fields['location'].widget.attrs['placeholder'] = 'Country & City'
		self.fields['github'].widget.attrs['placeholder'] = 'Github username'
		self.fields['facebook'].widget.attrs['placeholder'] = 'facebook link'
		self.fields['instagram'].widget.attrs['placeholder'] = 'instagram link'
		self.fields['twitter'].widget.attrs['placeholder'] = 'twitter link'
		self.fields['youtube'].widget.attrs['placeholder'] = 'youtube link'

		self.fields['location'].widget.attrs['class'] = 'form-control'
		self.fields['github'].widget.attrs['class'] = 'form-control'
		self.fields['facebook'].widget.attrs['class'] = 'form-control'
		self.fields['instagram'].widget.attrs['class'] = 'form-control'
		self.fields['twitter'].widget.attrs['class'] = 'form-control'
		self.fields['youtube'].widget.attrs['class'] = 'form-control'



	class Meta:
		model = UserProfile
		fields = ['avatar_pic', 'birth_date', 'github', 'location', 'facebook', 'instagram', 'twitter', 'youtube']

		widgets = {
			'avatar_pic': forms.FileInput(attrs={'class': 'form-control', 'type': 'file'}),
			'birth_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'value': datetime.now().strftime("%Y-%m-%d")}),
		}

	