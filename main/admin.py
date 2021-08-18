from django.contrib import admin

from .models import *


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
	list_display = ('announc', 'announc_from', 'announc_to')	
