from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.contrib import messages

from datetime import datetime

from .forms import SearchForm

from .services import get_most_posts, get_new_users, get_staff_members, get_most_likes, get_most_replies

def members(request):
	newest_users = get_new_users()
	most_posts = get_most_posts()
	most_replies = get_most_replies()
	most_likes = get_most_likes()
	staff_members = get_staff_members()

	now =  datetime.now()

	if request.method == 'POST':
		form = SearchForm(request.POST)

		if form.is_valid():
			username = form.cleaned_data['username']
			try:
				user = User.objects.get(username=username)
				return redirect('profile', username=user.username)
			except:
				messages.error(request, 'User with this username doesn\'t exist.')	
	else:
		form = SearchForm()	

	data = {
		'newest_users': newest_users,
		'now': now,
		'form': form,
		'most_posts': most_posts,
		'most_replies': most_replies,
		'staff_members': staff_members,
		'most_likes': most_likes,
	}
	return render(request, 'members/members.html', data)


def all_members(request):
	all_users = User.objects.all()
	now =  datetime.now()

	# Pagination
	pg = Paginator(all_users, 20)
	page = request.GET.get('page')
	users = pg.get_page(page)
	page_nums = 'n' * users.paginator.num_pages

	data = {
		'users': users,
		'page_nums': page_nums,
		'now': now,
	}
	return render(request, 'members/all_members.html', data)