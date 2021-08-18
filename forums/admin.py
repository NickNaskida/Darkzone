from django.contrib import admin
from .models import *


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
	list_display = ('category_name', 'category_description')


@admin.register(CategoryThreads)
class CategoryThreadsAdmin(admin.ModelAdmin):
	list_display = ('category', 'category_thread_name', 'category_thread_type')
	list_filter = ('category_thread_type',)
	search_fields = ('category__category_name', 'category_thread_name')
	
@admin.register(ThreadPosts)
class ThreadPostsAdmin(admin.ModelAdmin):
	list_display = ('author', 'thread', 'post_title', 'post_date', 'post_prefix')
	list_filter = ('post_prefix', 'post_date')
	search_fields = ('author__username', 'author__first_name', 'author__last_name', 'thread__category_thread_name', 'post_title')	

@admin.register(PostReplys)
class ThreadPostsAdmin(admin.ModelAdmin):
	list_display = ('post', 'reply_author', 'reply_date')
	list_filter = ('reply_date',)	


@admin.register(TagColors)
class TagColorsAdmin(admin.ModelAdmin):
	list_display = ('tag_color',)
	