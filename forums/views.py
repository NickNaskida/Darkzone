from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from django.utils.text import slugify
from django.contrib import messages
from django.core.paginator import Paginator

from datetime import datetime

from .models import Categories, CategoryThreads, ThreadPosts, PostReplys
from .forms import AddCategoryForm, AddCategoryThreadForm, AddPostForm, AddReplyForm, RemoveForm
from .filters import post_filter

from users.decorators import user_has_permission
from .services import get_categories, get_group_permissions, new_post_list, new_replies_list

from notifications.signals import notify

def forums(request):
	categories = get_categories()
	try:
		permissions = get_group_permissions(request.user)
	except:
		permissions = []

	threads = CategoryThreads.objects.all().order_by('pk')
	new_posts = new_post_list()				

	data = {
		'categories': categories,
		'permissions': permissions,
		'threads': threads,
		'new_posts': new_posts,
	}
	
	return render(request, 'forums/forums.html', data)


@user_has_permission('Can add Category')
@login_required
def add_category(request):
	if request.method == 'POST': 
		form = AddCategoryForm(request.POST)

		if form.is_valid():
			form.save()		
			return redirect('forums')
	else:
		form = AddCategoryForm()


	categories = get_categories()
	new_posts = new_post_list()	
	threads = CategoryThreads.objects.all()
	try:
		permissions = get_group_permissions(request.user)
	except:
		permissions = []


	data = {
		'form': form,
		'categories': categories,
		'permissions': permissions,
		'threads': threads,
		'new_posts': new_posts,
	}

	return render(request, 'forums/add_category.html', data)


@user_has_permission('Can change Category')
@login_required
def edit_category(request, pk):
	try:
		item = Categories.objects.get(pk=pk)	

		if request.method == 'POST': 
			form = AddCategoryForm(request.POST, instance=item)

			if form.is_valid():
				form.save()		
				return redirect('forums')
		else:
			form = AddCategoryForm(instance=item)


		categories = get_categories()
		new_posts = new_post_list()	
		threads = CategoryThreads.objects.all()
		try:
			permissions = get_group_permissions(request.user)
		except:
			permissions = []


		data = {
			'form': form,
			'categories': categories,
			'permissions': permissions,
			'threads': threads,
			'new_posts': new_posts,
		}

		return render(request, 'forums/add_category.html', data)
	except ObjectDoesNotExist:
		raise Http404("Item does not exist")


@user_has_permission('Can add Main Thread')
@login_required			
def add_category_thread(request):
	if request.method == 'POST': 
		form = AddCategoryThreadForm(request.POST)

		data = request.POST
		data._mutable = True
		data['category_thread_slug'] = slugify(data['category_thread_name'])
		data._mutable = False


		if form.is_valid():
			form.save()		
			return redirect('forums')
	else:
		form = AddCategoryThreadForm()


	categories = get_categories()
	new_posts = new_post_list()	
	threads = CategoryThreads.objects.all()
	try:
		permissions = get_group_permissions(request.user)
	except:
		permissions = []	

	data = {
		'form': form,
		'categories': categories,
		'permissions': permissions,
		'threads': threads,
		'new_posts': new_posts,	
	}

	return render(request, 'forums/add_category_thread.html', data)


@user_has_permission('Can change Main Thread')
@login_required
def edit_category_thread(request, pk):
	try:
		item = CategoryThreads.objects.get(pk=pk)
	except ObjectDoesNotExist:
		raise Http404("Item does not exist")		

	if request.method == 'POST': 
		form = AddCategoryThreadForm(request.POST, instance=item)

		data = request.POST
		data._mutable = True
		data['category_thread_slug'] = slugify(data['category_thread_name'])		
		data._mutable = False

		if form.is_valid():
			form.save()		
			return redirect('forums')
	else:
		form = AddCategoryThreadForm(instance=item)


	categories = get_categories()
	new_posts = new_post_list()	
	threads = CategoryThreads.objects.all()
	try:
		permissions = get_group_permissions(request.user)
	except:
		permissions = []


	data = {
		'form': form,
		'categories': categories,
		'permissions': permissions,
		'threads': threads,
		'new_posts': new_posts,
	}

	return render(request, 'forums/add_category_thread.html', data)
	

					
def category_thread(request, thread):
	try:
		item = CategoryThreads.objects.get(category_thread_slug=thread)
	except ObjectDoesNotExist:
		raise Http404("Thread does not exist")	

	try:
		permissions = get_group_permissions(request.user)
	except:
		permissions = []

	posts = ThreadPosts.objects.filter(thread=item).order_by('post_date')

	PostFilter = post_filter(request.GET, queryset= posts) 
	posts = PostFilter.qs

	# Pagination
	pg = Paginator(posts, 20)
	page = request.GET.get('page')
	thread_posts = pg.get_page(page)
	page_nums = 'n' * thread_posts.paginator.num_pages
		
	form = AddPostForm()

	if request.user.is_authenticated:
		if 'Can add Thread Post' in permissions:
			if item.category_thread_type == 'Private':
				if 'Can view private thread' in permissions:
					if request.method == 'POST': 
						form = AddPostForm(request.POST)

						data = request.POST
						data._mutable = True
						data['author'] = request.user
						data['thread'] = item
						data['post_slug'] = slugify(data['post_slug'])
						data['post_date'] = datetime.now()
						data['post_status'] = 'Open'
						data._mutable = False

						if form.is_valid():
							post = form.save()
							return redirect('thread_post', thread=post.thread.category_thread_slug, post=post.post_slug)				
			else:
				if request.method == 'POST': 
					form = AddPostForm(request.POST)

					data = request.POST
					data._mutable = True
					data['author'] = request.user
					data['thread'] = item
					data['post_slug'] = slugify(data['post_slug'])
					data['post_date'] = datetime.now()
					data['post_status'] = 'Open'
					data._mutable = False

					if form.is_valid():
						post = form.save()		
						return redirect('thread_post', thread=post.thread.category_thread_slug, post=post.post_slug)		

	data = {
		'item': item,
		'permissions': permissions,
		'form': form,
		'thread_posts': thread_posts,
		'page_nums': page_nums,
		'filter': PostFilter,
	}
	return render(request, 'forums/category_thread.html', data)



def thread_post(request, thread, post):
	try:
		item = ThreadPosts.objects.get(post_slug=post)
	except ObjectDoesNotExist:
		raise Http404("Post does not exist")	

	try:
		permissions = get_group_permissions(request.user)
	except:
		permissions = []

	if item.thread.category_thread_type == 'Private':
		if request.user.is_authenticated:
			if 'Can view private thread' not in permissions:
				raise Http404("Post does not exist")
		else:		
			raise Http404("Post does not exist")

	form = AddReplyForm()		
			
	if request.user.is_authenticated:
		if item.post_status == 'Open':
			if 'Can add Post Reply' in permissions:		
				if request.method == 'POST': 
					form = AddReplyForm(request.POST)

					data = request.POST
					data._mutable = True
					data['post'] = item
					data['reply_author'] = request.user
					data['reply_date'] = datetime.now()
					data._mutable = False

					if form.is_valid():
						reply = form.save()
						messages.success(request, f'Reply added successfully. <a href="#reply_{reply.pk}">Click here to see reply</a>')																			
						return redirect('thread_post', thread=item.thread.category_thread_slug, post=item.post_slug)


	replies = PostReplys.objects.filter(post=item)
	new_replies = new_replies_list(item)
	try:
		last_reply = replies.order_by('-reply_date')[0]
	except:
		last_reply = 0	
					
	data = {
		'item': item,
		'form': form,
		'permissions': permissions,
		'replies': replies,
		'last_reply': last_reply,
		'new_replies': new_replies,
	}
	return render(request, 'forums/post.html', data)


@login_required
def reply(request, thread, post, pk):
	try:
		item = ThreadPosts.objects.get(post_slug=post)
		reply_obj = PostReplys.objects.get(id=pk)
	except ObjectDoesNotExist:
		raise Http404("Reply does not exist")	

	try:
		permissions = get_group_permissions(request.user)
	except:
		permissions = []

	if item.thread.category_thread_type == 'Private':
		if 'Can view private thread' not in permissions:
			raise Http404("Post does not exist")
	
	if item.post_status == 'Closed':
		raise Http404("Post does not exist")	

	form = AddReplyForm()		

	if request.user.is_authenticated:
		if item.post_status == 'Open':
			if 'Can add Post Reply' in permissions:		
				if request.method == 'POST': 
					form = AddReplyForm(request.POST)
					
					data = request.POST
					data._mutable = True
					data['post'] = item
					data['reply_author'] = request.user
					data['reply_date'] = datetime.now()
					data._mutable = False

					if form.is_valid():
						reply = form.save(commit=False)
						reply.reply_parent = reply_obj
						reply.save()
						messages.success(request, f'Reply added successfully. <a href="#reply_{reply.pk}">Click here to see reply</a>')																		
						return redirect('thread_post', thread=item.thread.category_thread_slug, post=item.post_slug)

		
	replies = PostReplys.objects.filter(post=item)				

	data = {
		'item': item,
		'form': form,
		'permissions': permissions,
		'replies': replies,
		'reply': reply_obj,
	}
	return render(request, 'forums/reply.html', data)


@login_required
def change_post_status(request, thread, post, pk):
	try:
		item = ThreadPosts.objects.get(post_slug=post)
	except ObjectDoesNotExist:
		raise Http404("Post does not exist")

	try:
		permissions = get_group_permissions(request.user)
	except:
		permissions = []

	if request.user == 	item.author or 'Moder can change post status' in permissions:
		if item.post_status == 'Closed':
			item.post_status = 'Open'
			item.save()
		else:	
			item.post_status = 'Closed'
			item.save()
		return redirect('thread_post', thread=item.thread.category_thread_slug, post=item.post_slug)	
	else:
		raise Http404()


# Post like views
@login_required		
def like_post(request, thread, post, pk):
	try:
		item = ThreadPosts.objects.get(id=pk)
	except:
		raise Http404("Post does not exist")

	if item.thread.category_thread_type == 'Private':	
		try:
			permissions = get_group_permissions(request.user)
		except:
			permissions = []

		if 'Can view private thread' not in permissions:
			raise Http404("Post does not exist")		
			
	item.post_likes.add(request.user)
	return redirect('thread_post', thread=item.thread.category_thread_slug, post=item.post_slug)


@login_required		
def unlike_post(request, thread, post, pk):
	try:
		item = ThreadPosts.objects.get(id=pk)
	except:
		raise Http404("Post does not exist")

	if item.thread.category_thread_type == 'Private':	
		try:
			permissions = get_group_permissions(request.user)
		except:
			permissions = []

		if 'Can view private thread' not in permissions:
			raise Http404("Post does not exist")	

	item.post_likes.remove(request.user)
	return redirect('thread_post', thread=item.thread.category_thread_slug, post=item.post_slug)	


# Reply like views
@login_required		
def like_reply(request, thread, post, pk):
	try:
		item = PostReplys.objects.get(id=pk)
	except:
		raise Http404("Reply does not exist")

	if item.post.thread.category_thread_type == 'Private':	
		try:
			permissions = get_group_permissions(request.user)
		except:
			permissions = []

		if 'Can view private thread' not in permissions:
			raise Http404("Post does not exist")		
			
	item.reply_likes.add(request.user)
	return redirect('thread_post', thread=item.post.thread.category_thread_slug, post=item.post.post_slug)


@login_required		
def unlike_reply(request, thread, post, pk):
	try:
		item = PostReplys.objects.get(id=pk)
	except:
		raise Http404("Reply does not exist")

	if item.post.thread.category_thread_type == 'Private':	
		try:
			permissions = get_group_permissions(request.user)
		except:
			permissions = []

		if 'Can view private thread' not in permissions:
			raise Http404("Post does not exist")	

	item.reply_likes.remove(request.user)
	return redirect('thread_post', thread=item.post.thread.category_thread_slug, post=item.post.post_slug)	

# Delete

@login_required	
def delete_post(request, thread, post, pk):
	try:
		item = ThreadPosts.objects.get(id=pk)
	except:
		raise Http404("Post does not exist")

	if request.user == item.author:	
		if request.method == 'POST':
			item.delete()
			messages.success(request, 'Deleted successfully.')
			return redirect('forums')
	else:
		raise Http404()	


@login_required	
def delete_reply(request, thread, post, pk):
	try:
		item = PostReplys.objects.get(id=pk)
	except:
		raise Http404("Post does not exist")

	if request.user == item.reply_author:	
		if request.method == 'POST':
			item.delete()
			messages.success(request, 'Deleted successfully.')
			return redirect('thread_post', thread=item.post.thread.category_thread_slug, post=item.post.post_slug)
	else:
		raise Http404()				


# Edit
@login_required								
def edit_post(request, thread, post, pk):
	try:
		item = ThreadPosts.objects.get(id=pk)
	except:
		raise Http404("Post does not exist")

	if item.author == request.user:
		if request.method == 'POST': 
			form = AddPostForm(request.POST, instance=item)

			if form.is_valid():
				post = form.save()
				messages.success(request, 'Edited successfully.')		
				return redirect('thread_post', thread=post.thread.category_thread_slug, post=post.post_slug)
		else:
			form = AddPostForm(instance=item)
	else:		
		raise Http404()

	data = {
		'form': form,
		'item': item,
	}
	return render(request, 'forums/edit_post.html', data)


@login_required								
def edit_reply(request, thread, post, pk):
	try:
		reply = PostReplys.objects.get(id=pk)
		item = reply.post
	except:
		raise Http404("Post does not exist")

	if reply.reply_author == request.user:
		if request.method == 'POST': 
			form = AddReplyForm(request.POST, instance=reply)

			if form.is_valid():
				reply = form.save()
				messages.success(request, 'Edited successfully.')		
				return redirect('thread_post', thread=reply.post.thread.category_thread_slug, post=reply.post.post_slug)
		else:
			form = AddReplyForm(instance=reply)
	else:		
		raise Http404()

	data = {
		'form': form,
		'reply': reply,
		'item': item,
	}
	return render(request, 'forums/edit_reply.html', data)								


# Moderator remove	
@login_required								
def remove_post(request, thread, post, pk):
	try:
		item = ThreadPosts.objects.get(id=pk)
	except:
		raise Http404("Post does not exist")

	try:
		permissions = get_group_permissions(request.user)
	except:
		permissions = []

	if item.author.is_superuser:
		raise Http404()		

	if 'Moder can delete post' in permissions:	
		if item.author != request.user:
			if request.method == 'POST': 
				form = RemoveForm(request.POST)

				data = request.POST

				if form.is_valid():
					item.delete()

					notify.send(
						item.author,
						recipient=item.author,
						verb='ban',
					 	description=f'"{item.post_title}" was removed by {request.user}. Remove reason: ' + data['remove_reason']
						)

					messages.success(request, 'Removed successfully')		
					return redirect('category_thread', thread=item.thread.category_thread_slug)
			else:
				form = RemoveForm()
		else:		
			raise Http404()
	else:		
		raise Http404()

	data = {
		'form': form,
		'item': item,
	}
	return render(request, 'forums/remove_post.html', data)


@login_required								
def remove_reply(request, thread, post, pk):
	try:
		reply = PostReplys.objects.get(id=pk)
		item = reply.post
	except:
		raise Http404("Post does not exist")

	try:
		permissions = get_group_permissions(request.user)
	except:
		permissions = []

	if reply.reply_author.is_superuser:
		raise Http404()		

	if 'Moder can delete reply' in permissions:	
		if reply.reply_author != request.user:
			if request.method == 'POST': 
				form = RemoveForm(request.POST)

				data = request.POST

				if form.is_valid():
					reply.delete()

					notify.send(
						reply.reply_author,
						recipient=reply.reply_author,
						verb='ban',
					 	description=f'Your reply at post "{reply.post.post_title}" was removed by {request.user}. Remove reason: ' + data['remove_reason']
						)

					messages.success(request, 'Removed successfully')		
					return redirect('thread_post', thread=reply.post.thread.category_thread_slug, post=reply.post.post_slug)
			else:
				form = RemoveForm()
		else:		
			raise Http404()
	else:		
		raise Http404()

	data = {
		'form': form,
		'reply': reply,
		'item': item,
	}
	return render(request, 'forums/remove_reply.html', data)	
