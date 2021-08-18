from django.urls import path
from . import views

urlpatterns = [
	path('', views.main, name='home'),
	path('terms&rules', views.terms, name='terms&rules'),
	path('privacy-policy', views.privacy_policy, name='privacy_policy'),
]