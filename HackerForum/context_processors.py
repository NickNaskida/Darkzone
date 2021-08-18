from datetime import timedelta
import online_users.models as onl
import hashlib
from datetime import datetime

from django.contrib.auth.models import User
from forums.models import ThreadPosts, PostReplys, CategoryThreads
from main.models import Announcement
from forums.models import TagColors

def online_users(request):
	user_activity_objects = onl.OnlineUserActivity.get_user_activities(timedelta(minutes=10)).reverse()
	online_users = []

	for user in user_activity_objects:
		online_users.append(user)

	if len(online_users) != 0:
		online_users_count = len(online_users)
	else:
		online_users_count = 0

	if len(online_users) != 0:	
		last_online_user = online_users[-1]	
	else:
		last_online_user = 0


	users = User.objects.all().count()
	replies = PostReplys.objects.all().count()
	posts = ThreadPosts.objects.all().count()
	threads = CategoryThreads.objects.all().count()
	
	now = datetime.now()
	try:
		announc = Announcement.objects.filter(announc_from__lte=now, announc_to__gte=now)[0] 
	except:
		announc = None

	tag_colors = TagColors.objects.all()
	tag_colors_list = []

	for color in tag_colors:
		tag_colors_list.append(color.tag_color)
		
	'''	
	signature = ''	
	if request.user.is_authenticated:
		user = str(request.user.id) + request.user.first_name + ' ' + request.user.last_name
		permissions = 'deleteban'
		avatar_url = 'http://127.0.0.1:8000' + request.user.userprofile.avatar_pic.url
		profile_url = 'http://127.0.0.1:8000/profile/' + request.user.username
		secret_key = 'a7207d82-56d7-4a2d-95b7-dc539986f9e2'

		try:
			color = request.user.userrole.role.color
		except:
			color = ''	

		string = 'http:127.0.0.1' + user + avatar_url + profile_url + color + permissions + secret_key
		signature = hashlib.md5(string.encode()).hexdigest()

		#print(string)

	'''	


	return {
		'online_users': online_users,
		'online_users_count': online_users_count,
		'last_online_user': last_online_user,
		'users_cnt': users,
		'replies_cnt': replies,
		'posts_cnt': posts,
		'threads_cnt': threads,
		'announc': announc,
		'tag_colors_list': tag_colors_list,
		#'signature': signature,
	}