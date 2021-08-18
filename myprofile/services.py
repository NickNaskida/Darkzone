from django.db.models import Count, Sum

import online_users.models as onl
from datetime import timedelta

from forums.models import ThreadPosts, PostReplys


def user_online_status(user_data):
	'''User online status calculation'''
	user_online = False

	user_activity_objects = onl.OnlineUserActivity.get_user_activities(timedelta(minutes=10))
	online_users = []

	for user in user_activity_objects:
		online_users.append(user)

	for i in online_users:
		if i.user.username == user_data.username:
			user_online = True	
			break

	return user_online		


def	posts_percentage(user_data):
	total_posts = ThreadPosts.objects.all().count()
	user_posts = user_data.user_posts.all().count()
	if total_posts != 0:
		ans = (user_posts / total_posts) * 100
		return round(ans, 2)
	else:
		return 0	


def	messages_percentage(user_data):
	total_messages = PostReplys.objects.all().count()
	user_messages = user_data.user_replies.all().count()
	if total_messages != 0:
		ans = (user_messages / total_messages) * 100
		return round(ans, 2)
	else:
		return 0


def total_likes(user_data):
	post_likes = ThreadPosts.objects.filter(author=user_data).annotate(num_likes=Count('post_likes')) \
		.aggregate(Sum('num_likes'))['num_likes__sum']
	reply_likes = PostReplys.objects.filter(reply_author=user_data).annotate(num_likes=Count('reply_likes')) \
		.aggregate(Sum('num_likes'))['num_likes__sum']

	if post_likes == None:
		post_likes = 0
	if reply_likes == None:
		reply_likes = 0

	ans = post_likes + reply_likes
	return ans	


def likes_percentage(user_data):
	user_likes = total_likes(user_data)
	all_post_likes = ThreadPosts.objects.all().annotate(num_likes=Count('post_likes')) \
		.aggregate(Sum('num_likes'))['num_likes__sum']
	all_reply_likes = PostReplys.objects.all().annotate(num_likes=Count('reply_likes')) \
		.aggregate(Sum('num_likes'))['num_likes__sum']

	if all_post_likes == None:
		all_post_likes = 0
	if all_reply_likes == None:
		all_reply_likes = 0

	all_likes = all_post_likes + all_reply_likes

	if all_likes != 0:
		ans = (user_likes / all_likes) * 100
		return round(ans, 2)
	else:
		return 0	

