from django.shortcuts import redirect
from forums.services import get_group_permissions
from django.http import Http404

def unauthenticated_user(view_func):
	def wrapper_func(request, *args, **kwargs):
		if request.user.is_authenticated:
			return redirect('home')
		else:
			return view_func(request, *args, **kwargs)
	return wrapper_func


def user_has_permission(perm):
	def decorator(view_func):
		def wrapper_func(request, *args, **kwargs):
			if request.user.is_authenticated:
				try:
					permissions_list = get_group_permissions(request.user)
				except:
					permissions_list = []

				if perm in permissions_list:
					return view_func(request, *args, **kwargs)
				else:
					raise Http404("Page does not exist")	
			else:
				return redirect('login')
		return wrapper_func		
	return decorator	