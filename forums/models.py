from django.db import models
from django.contrib.auth.models import User

from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

from taggit.managers import TaggableManager
from colorfield.fields import ColorField

class Categories(models.Model):
	category_name = models.CharField(max_length=25)
	category_description = models.CharField(max_length=80, blank=True)

	def __str__(self):
		return self.category_name

	class Meta:
		verbose_name = 'Category'
		verbose_name_plural = 'Categories'


class CategoryThreads(models.Model):
	category = models.ForeignKey(Categories, on_delete=models.PROTECT, related_name='thread_category', null=True)
	category_thread_name = models.CharField(max_length=25, unique=True, null=True)
	category_thread_description = models.CharField(max_length=60, blank=True, null=True)
	category_thread_type = models.CharField(max_length=20, null=True)
	category_thread_slug = models.SlugField(unique=True, null=True)
	category_thread_icon = models.CharField(max_length=60, null=True)


	def __str__(self):
		return self.category_thread_name

	class Meta:
		permissions = [
            ("view_private_thread", "Can view private thread"),
        ]

		verbose_name = 'Main Thread'
		verbose_name_plural = 'Main Threads'


class ThreadPosts(models.Model):
	author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_posts', null=True)
	thread = models.ForeignKey(CategoryThreads, on_delete=models.PROTECT, related_name='thread_posts', null=True)
	post_title = models.CharField(max_length=60, unique=True, null=True)
	post_slug = models.SlugField(unique=True, null=True)
	post_date = models.DateTimeField(auto_now=False, auto_now_add=False, null=True)
	post_prefix = models.CharField(max_length=20, null=True)
	post_status = models.CharField(max_length=20, null=True)
	post_body = RichTextUploadingField(null=True)
	post_likes = models.ManyToManyField(User, related_name='user_likes', blank=True)
	post_tags = TaggableManager()
	
	def __str__(self):
		return self.post_title

	class Meta:
		permissions = [
            ("change_status", "Moder can change post status"),
            ("moder_post_delete", "Moder can delete post"),
        ]

		verbose_name = 'Thread Post'
		verbose_name_plural = 'Thread Posts'


class PostReplys(models.Model):
	post = models.ForeignKey(ThreadPosts, on_delete=models.CASCADE, related_name='post_replies', null=True)
	reply_author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_replies', null=True)
	reply_parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
	reply_date = models.DateTimeField(auto_now=False, auto_now_add=False, null=True)
	reply_body = RichTextUploadingField(null=True)
	reply_likes = models.ManyToManyField(User, related_name='user_reply_likes', blank=True)

	class Meta:
		permissions = [
            ("moder_reply_delete", "Moder can delete reply"),
        ]

		verbose_name = 'Post Reply'
		verbose_name_plural = 'Post Replys'


class TagColors(models.Model):
	tag_color = ColorField()

	class Meta:
		verbose_name = 'Tag Color'
		verbose_name_plural = 'Tag Colors'