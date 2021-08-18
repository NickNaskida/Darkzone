from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import UserRegisterForm

from .decorators import unauthenticated_user

from notifications.signals import notify

@unauthenticated_user
def register(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			item = form.save()
			messages.success(request, f'Account created for {item.username}')
			notify.send(item, recipient=item, verb='notification', description='Thanks for registration, you can request your badges in live chat.')

			return redirect('login')
	else:
		form = UserRegisterForm()
	
	return render(request, 'users/register.html', {'form': form})
