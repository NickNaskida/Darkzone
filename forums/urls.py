from django.urls import path
from . import views

urlpatterns = [
	path('', views.forums, name='forums'),

	path('add-category', views.add_category, name='add_category'),
	path('<str:pk>/edit-category', views.edit_category, name='edit_category'),

	path('add-category-thread', views.add_category_thread, name='add_category_thread'),
	path('<str:pk>/edit-category-thread', views.edit_category_thread, name='edit_category_thread'),

	path('<str:thread>/', views.category_thread, name='category_thread'),
	path('<str:thread>/<str:post>', views.thread_post, name='thread_post'),

	path('<str:thread>/<str:post>/like/<str:pk>', views.like_post, name='like_post'),
	path('<str:thread>/<str:post>/remove-like/<str:pk>', views.unlike_post, name='unlike_post'),
	path('<str:thread>/<str:post>/like-reply/<str:pk>', views.like_reply, name='like_reply'),
	path('<str:thread>/<str:post>/remove-reply-like/<str:pk>', views.unlike_reply, name='unlike_reply'),

	path('<str:thread>/<str:post>/reply/<str:pk>', views.reply, name='reply'),

	path('<str:thread>/<str:post>/change-status/<str:pk>', views.change_post_status, name='change_post_status'),

	path('<str:thread>/<str:post>/delete_post/<str:pk>', views.delete_post, name='delete_post'),
	path('<str:thread>/<str:post>/delete_reply/<str:pk>', views.delete_reply, name='delete_reply'),

	path('<str:thread>/<str:post>/edit_post/<str:pk>', views.edit_post, name='edit_post'),
	path('<str:thread>/<str:post>/edit_reply/<str:pk>', views.edit_reply, name='edit_reply'),

	path('<str:thread>/<str:post>/remove_post/<str:pk>', views.remove_post, name='remove_post'),
	path('<str:thread>/<str:post>/remove_reply/<str:pk>', views.remove_reply, name='remove_reply'),
]