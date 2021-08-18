from django import forms

class SearchForm(forms.Form):
    username = forms.CharField(label = '',  widget=forms.TextInput(attrs={'placeholder': 'Username'}), max_length=150)