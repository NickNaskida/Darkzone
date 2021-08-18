from users.models import Roles
from forums.models import ThreadPosts

def get_roles():
	return Roles.objects.all()

def get_common_tags():
	return ThreadPosts.post_tags.most_common()[:30]

