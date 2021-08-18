from django.shortcuts import render
from django.contrib.auth.models import User

from .services import get_roles, get_common_tags

from datetime import datetime
from urllib.request import urlopen

from forums.models import ThreadPosts, PostReplys, CategoryThreads


def main(request):
	user_ip = urlopen('http://ip.42.pl/raw').read().decode("utf-8")  #get_client_ip(request)

	server_time =  datetime.now()

	users = User.objects.all().count()
	replies = PostReplys.objects.all().count()
	posts = ThreadPosts.objects.all().count()
	threads = CategoryThreads.objects.all().count()

	popular_tags = get_common_tags()
	last_posts = ThreadPosts.objects.filter(thread__category_thread_type='Public').order_by('-post_date')[:6]

	data = {
		'user_ip': user_ip,
		'server_time': server_time, 
		'users': users,
		'replies': replies,
		'posts': posts,
		'threads': threads,
		'last_posts': last_posts,
		'popular_tags': popular_tags,
	}
	return render(request, 'main/index.html', data)

def terms(request):
	roles = get_roles()

	data = {
		'roles': roles,
	}
	return render(request, 'main/terms&rules.html', data)	

def privacy_policy(request):	
	return render(request, 'main/policy.html')	

def error_404(request, exception):
    return render(request, 'main/404.html', {"exc": exception})
