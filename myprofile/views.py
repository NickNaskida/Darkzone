from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.core.files.storage import FileSystemStorage

from datetime import datetime

from users.models import UserProfile 

from .services import user_online_status, posts_percentage, messages_percentage, total_likes, likes_percentage


def profile(request, username):
	try:
		user_data = User.objects.get(username=username)
		profile_data = UserProfile.objects.get(user=user_data.id)
	except ObjectDoesNotExist:
		raise Http404("Profile does not exist")	
							
	user_online = user_online_status(user_data)

	posts_perc = posts_percentage(user_data)
	messages_perc = messages_percentage(user_data)	
	likes_perc = likes_percentage(user_data)
	likes_received = total_likes(user_data)

	user_last_posts = user_data.user_posts.filter(thread__category_thread_type='Public').order_by('-post_date')[:7]
	
	now = datetime.now()

	data = {
		'user_data': user_data,
		'user_online': user_online,
		'posts_percentage': posts_perc,
		'messages_percentage': messages_perc,
		'likes_received': likes_received,
		'likes_perc': likes_perc,
		'user_last_posts': user_last_posts,
		'now': now,
	}
	return render(request, 'myprofile/myprofile.html', data)


@login_required
def login_redirect(request):
	return HttpResponseRedirect(f'{request.user.username}')
