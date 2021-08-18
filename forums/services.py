from datetime import datetime, timedelta

from .models import Categories, ThreadPosts, PostReplys

def get_categories():
	categories = Categories.objects.all()
	return categories
	

def get_group_permissions(user):
	permissions_list = []
	permissions = user.groups.get(name=user.userrole.role).permissions.all()
	
	for i in permissions:
		permissions_list.append(i.name)
	return permissions_list

def new_post_list():
	new_posts = []

	period = datetime.now()-timedelta(hours=24)
	posts = ThreadPosts.objects.filter(post_date__gte=period)

	for post in posts:
		new_posts.append(post.thread.pk)

	return(new_posts)


def new_replies_list(item):
	new_replies = []

	period = datetime.now()-timedelta(hours=24)
	replies = PostReplys.objects.filter(post=item, reply_date__gte=period)

	for reply in replies:
		new_replies.append(reply.pk)

	return(new_replies)		



	
