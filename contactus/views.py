from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import ContactForm

from .services import send_email

def contactus(request):
	if request.method == 'POST':   
	    form = ContactForm(request.POST)
	    if form.is_valid():
	        name = form.cleaned_data['name']
	        email = form.cleaned_data['email']
	        message = form.cleaned_data['message'] + f"\n\nDarkZone, sender: {email}"	

	        send_email(name, email, message)
	        
	        messages.success(request, f'Thanks {name}! We received your email and will respond shortly...')	
	        return redirect('contactus')	
	else:
		form = ContactForm()

	data = {
		'form': form,
	}
	return render(request, 'contactus/contactus.html', data)
