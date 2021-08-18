from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

from colorfield.fields import ColorField

class Roles(models.Model):
	role_group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='group_role', null=True)
	role = models.CharField(max_length=50, null=True)
	color = ColorField()
	description = models.TextField(null=True)

	def __str__(self):
		return self.role

	class Meta:
		verbose_name = 'Role'
		verbose_name_plural = 'Roles'
					

class UserRole(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userrole')
	role = models.ForeignKey(Roles, on_delete=models.PROTECT)	

	class Meta:
		verbose_name = 'User Role'
		verbose_name_plural = 'User Roles'


class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile', null=True)
	slug = models.SlugField(unique=True, null=True)
	avatar_pic = models.ImageField(default='user.png', blank=True, null=True)
	birth_date = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
	location = models.CharField(max_length=20, null=True, blank=True)
	github = models.CharField(max_length=40, null=True, blank=True)
	facebook = models.URLField(null=True, blank=True)
	twitter = models.URLField(null=True, blank=True)
	instagram = models.URLField(null=True, blank=True)
	youtube = models.URLField(null=True, blank=True)
	

	class Meta:
		verbose_name = 'User Profile'
		verbose_name_plural = 'User Profiles'


class Badges(models.Model):
	badge = models.CharField(max_length=50, null=True)
	color = ColorField()

	def __str__(self):
		return self.badge

	class Meta:
		verbose_name = 'Badge'
		verbose_name_plural = 'Badges'


class UserBadge(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='userbadge')
	badge = models.ForeignKey(Badges, on_delete=models.PROTECT)	

	class Meta:
		verbose_name = 'User Badge'
		verbose_name_plural = 'User Badges'