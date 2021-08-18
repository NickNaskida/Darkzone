from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from datetime import datetime

@login_required
def notifications(request):
	user = request.user
	user.notifications.mark_all_as_read()

	notifications = user.notifications.read()[:30]

	now = datetime.now()

	data = {
		'notifications': notifications,
		'now': now,
	}
	return render(request, 'notify/notifications.html', data)






