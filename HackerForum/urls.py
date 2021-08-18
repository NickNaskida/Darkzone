from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url

from django.contrib.auth import views as auth_views
from users import views as user_views

from django.conf.urls.static import static
from django.conf import settings

import notifications.urls

from myprofile import views

from django.conf.urls import handler404

# Ckeditor
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from ckeditor_uploader import views as ckeditor_views


urlpatterns = [
    path('ckeditor/upload/', login_required(ckeditor_views.upload), name='ckeditor_upload'),
    path('ckeditor/browse/', never_cache(login_required(ckeditor_views.browse)), name='ckeditor_browse'),

    path('dz-admin/', admin.site.urls),
    path('admin/defender/', include('defender.urls')), # defender admin
    
    path('', include('main.urls')),
    path('contact-us', include('contactus.urls')),
    path('profile/<str:username>', include('myprofile.urls')),
    path('forums/', include('forums.urls')),
    path('notifications', include('notify.urls')),
    path('members/', include('members.urls')),
    path('settings/', include('settings.urls')),

    path('signup', include('users.urls')),
    path('login', auth_views.LoginView.as_view(template_name='users/login.html', redirect_authenticated_user=True), name='login'),
    path('logout', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('profile/', views.login_redirect, name='profile_redirect'),

    url('^inbox/notifications/', include(notifications.urls, namespace='notifications')),

    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'), name='reset_password'),
    path('reset_password_resent/', auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_sent.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_form.html'), name='password_reset_confirm'),
    path('reset_password_complete', auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_done.html'), name='password_reset_complete'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'main.views.error_404'
