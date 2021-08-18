from django.db.models.signals import post_save, post_delete, pre_save, m2m_changed
from django.dispatch import receiver
from django.contrib.auth.models import User

from forums.models import ThreadPosts, PostReplys

from notifications.signals import notify


# Replies
@receiver(post_save, sender=PostReplys)
def send_reply_notification(sender, instance, created, **kwargs):
	if created:
		if instance.reply_parent:
			if instance.reply_parent.reply_author != instance.reply_author:
				notify.send(
					instance.reply_parent.reply_author,
					recipient=instance.reply_parent.reply_author,
					verb='reply',
				 	description=f'{instance.reply_author} replied on your reply.&nbsp;' + \
				 		'<a href="/forums/' + f'{instance.post.thread.category_thread_slug}/' + \
				 			f'{instance.post.post_slug}' + f'#reply_{instance.pk}' + '">See reply</a>',
				)
		else:
			if instance.post.author != instance.reply_author:	
				notify.send(
					instance.post.author,
					recipient=instance.post.author,
					verb='reply',
				 	description=f'{instance.reply_author} replied on your post "{instance.post.post_title}".&nbsp;' + \
				 		'<a href="/forums/' + f'{instance.post.thread.category_thread_slug}/' + \
				 			f'{instance.post.post_slug}' + f'#reply_{instance.pk}' + '">See reply</a>',
				)


# Likes
@receiver(m2m_changed, sender=ThreadPosts.post_likes.through)
def send_post_like_notification(sender, **kwargs):
	action = kwargs.pop('action', None)
	pk_set = kwargs.pop('pk_set', None)
	instance = kwargs.pop('instance', None)
		
	if action == "post_add":
		pk = list(pk_set)
		user = User.objects.get(id=pk[0])

		if instance.author != user:	
			notify.send(
				instance.author,
				recipient=instance.author,
				verb='like',
			 	description=f'{user.username} liked your post "{instance.post_title}".&nbsp;' + \
			 		'<a href="/forums/' + f'{instance.thread.category_thread_slug}/' + \
			 			f'{instance.post_slug}' + '">See post</a>',
			)


@receiver(m2m_changed, sender=PostReplys.reply_likes.through)
def send_reply_like_notification(sender, **kwargs):
	action = kwargs.pop('action', None)
	pk_set = kwargs.pop('pk_set', None)
	instance = kwargs.pop('instance', None)
	
	if action == "post_add":
		pk = list(pk_set)
		user = User.objects.get(id=pk[0])

		if instance.reply_author != user:	
			notify.send(
				instance.reply_author,
				recipient=instance.reply_author,
				verb='like',
			 	description=f'{user.username} liked your reply.&nbsp;' + \
			 		'<a href="/forums/' + f'{instance.post.thread.category_thread_slug}/' + \
			 			f'{instance.post.post_slug}' + f'#reply_{instance.pk}' + '">See reply</a>',
			)					



























'''
# Profile 
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
	if created:
		UserProfile.objects.create(user=instance, slug=instance.username)

# Group
@receiver(post_save, sender=Group)
def create_group(sender, instance, created, **kwargs):
	if created:
		Roles.objects.create(role_group=instance, role=f'{instance.name}')

@receiver(post_save, sender=Group)
def update_group(sender, instance, created, **kwargs):
	if created == False:
		item = Roles.objects.get(role_group=instance)
		item.role = instance.name
		item.save()



# UserRole
@receiver(post_save, sender=UserRole)
def add_user_to_group(sender, instance, created, **kwargs):		
	if created:
		group = Group.objects.get(name=instance.role)
		group.user_set.add(instance.user)

		#notification
		notify.send(
			instance.user,
			recipient=instance.user,
			verb='role',
		 	description=f'Congratulations! You were given&nbsp;<span style="color: {instance.role.color};">{instance.role}</span>&nbsp;role.&nbsp;' + '<a href="/profile/' + f'{instance.user.username}' + '">Go to profile</a>',
			action_object=instance
		)

@receiver(post_save, sender=UserRole)
def edit_user_group(sender, instance, created, **kwargs):		
	if created == False:
		instance.user.groups.clear()
		group = Group.objects.get(name=instance.role)
		group.user_set.add(instance.user)

		#notification
		ct = ContentType.objects.get(model='userrole')
		notification = instance.user.notifications.filter(action_object_object_id=instance.pk, action_object_content_type_id=ct)[0]
		notification.delete()

		notify.send(
			instance.user,
			recipient=instance.user,
			verb='role',
		 	description=f'Congratulations! You were given&nbsp;<span style="color: {instance.role.color};">{instance.role}</span>&nbsp;role.&nbsp;' + '<a href="/profile/' + f'{instance.user.username}' + '">Go to profile</a>',
			action_object=instance
		)

@receiver(post_delete, sender=UserRole)
def delete_user_group(sender, instance, **kwargs):		
	instance.user.groups.remove(instance.role.role_group)
	
	#notification
	notify.send(
			instance.user,
			recipient=instance.user,
			verb='unhappy',
		 	description=f'You aren\'t&nbsp;<span style="color: {instance.role.color};">{instance.role}</span>&nbsp;anymore.',
			action_object=instance
		)		


# UserBadge
@receiver(post_save, sender=UserBadge)
def badge_create(sender, instance, created, **kwargs):		
	if created:
		#notification
		notify.send(
			instance.user,
			recipient=instance.user,
			verb='badge',
		 	description=f'You have new badge - {instance.badge}.&nbsp;' + '<a href="/profile/' + f'{instance.user.username}' + '">Go to profile</a>',
			action_object=instance
		)

@receiver(post_save, sender=UserBadge)
def badge_edit(sender, instance, created, **kwargs):		
	if created == False:
		#notification
		ct = ContentType.objects.get(model='userbadge')
		notification = instance.user.notifications.filter(action_object_object_id=instance.pk, action_object_content_type_id=ct)[0]
		notification.delete()

		notify.send(
			instance.user,
			recipient=instance.user,
			verb='badge',
		 	description=f'You have new badge - {instance.badge}.&nbsp;' + '<a href="/profile/' + f'{instance.user.username}' + '">Go to profile</a>',
			action_object=instance
		)

@receiver(post_delete, sender=UserBadge)
def badge_delete(sender, instance, **kwargs):		
		#notification
		notify.send(
			instance.user,
			recipient=instance.user,
			verb='unhappy',
		 	description=f'You don\'t have {instance.badge} badge anymore', 
			action_object=instance
		)			

'''		