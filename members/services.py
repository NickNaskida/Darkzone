from django.contrib.auth.models import User
from django.db.models import Count

def get_new_users():
	ans = User.objects.all().order_by('-pk')[:10]
	return ans

def get_most_posts():
	ans = User.objects.annotate(num_posts=Count('user_posts')).order_by('-num_posts')[:5]
	return ans

def get_most_likes():
	ans = User.objects.annotate(likes_num=Count('user_likes', distinct=True) + Count('user_reply_likes', distinct=True)) \
		.order_by('-likes_num')[:5]
	return ans

def get_most_replies():
	ans = User.objects.annotate(num_replies=Count('user_replies')).order_by('-num_replies')[:5]
	return ans	

def get_staff_members():
	ans = User.objects.filter(userbadge__badge__badge='Staff member')[:5]
	return ans