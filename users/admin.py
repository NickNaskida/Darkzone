from django.contrib import admin

from .models import *


@admin.register(Roles)
class RolesAdmin(admin.ModelAdmin):
	list_display = ('role', 'color')	
	search_fields = ('role',)

@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
	list_display = ('user', 'role')
	list_filter = ('role',)
	search_fields = ('role__role', 'user__username')


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
	list_display = ('user',)
	search_fields = ('user__username', 'user__first_name', 'user__last_name')
	

@admin.register(Badges)
class BadgesAdmin(admin.ModelAdmin):
	list_display = ('badge', 'color')
	search_fields = ('badge',)

@admin.register(UserBadge)
class UserBadgeAdmin(admin.ModelAdmin):
	list_display = ('user', 'badge')
	list_filter = ('badge',)
	search_fields = ('badge__badge', 'user__username')	