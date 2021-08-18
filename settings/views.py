from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.contrib.auth.models import User
from users.models import UserProfile
from .forms import ProfileForm

@login_required
def settings(request):
	user = User.objects.get(id=request.user.pk)

	form = ProfileForm(instance=user.userprofile)	
	
	if request.method == 'POST':
		form = ProfileForm(request.POST, request.FILES, instance=user.userprofile)

		if form.is_valid():			
			form.save()
			messages.success(request, 'Settings saved successfully')
			return redirect('settings')

	data = {
		'form': form,
	}
	return render(request, 'settings/settings.html', data)
