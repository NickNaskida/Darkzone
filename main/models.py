from django.db import models

class Announcement(models.Model):
	announc = models.CharField(max_length=60)
	announc_from = models.DateTimeField(auto_now=False, auto_now_add=False)
	announc_to = models.DateTimeField(auto_now=False, auto_now_add=False)

