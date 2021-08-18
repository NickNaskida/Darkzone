import os
import json
from pathlib import Path
from datetime import timedelta
from django.contrib.messages import constants as messages

with open('/etc/dz-config.json') as config_file:
    config = json.load(config_file)    

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['192.168.0.11', 'localhost']


# Application definition

INSTALLED_APPS = [
    'admin_interface',

    'main.apps.MainConfig',
    'users.apps.UsersConfig',
    'contactus.apps.ContactusConfig',
    'myprofile.apps.MyprofileConfig',
    'forums.apps.ForumsConfig',
    'notify.apps.NotifyConfig',
    'members.apps.MembersConfig',
    'settings.apps.SettingsConfig',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'crispy_forms',
    'online_users',
    'defender',
    'notifications',
    'ckeditor',
    'ckeditor_uploader',
    'django_filters',
    'captcha',
    'colorfield',
    'taggit',
    #'axes',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'online_users.middleware.OnlineNowMiddleware',
    'defender.middleware.FailedLoginMiddleware',
    #'axes.middleware.AxesMiddleware',

]

AUTHENTICATION_BACKENDS = [
    #'axes.backends.AxesBackend',
    'django.contrib.auth.backends.ModelBackend',
]

ROOT_URLCONF = 'HackerForum.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'HackerForum.context_processors.online_users',
            ],
        },
    },
]

WSGI_APPLICATION = 'HackerForum.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {     
	'ENGINE': 'django.db.backends.postgresql_psycopg2',       
	'NAME': 'darkzone',       
	'USER': config['USER'],        
	'PASSWORD': config['PASSWORD'],        
	'HOST': 'localhost',       
	'PORT': '',    
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# admin interface
X_FRAME_OPTIONS='SAMEORIGIN'

# Security
CSRF_COOKIE_SAMESITE = 'Strict'

#SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
#SECURE_SSL_REDIRECT = True

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Tbilisi'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Django axes
# AXES_COOLOFF_TIME = timedelta(minutes=5)

# Django defender
DEFENDER_LOGIN_FAILURE_LIMIT = 5
DEFENDER_LOCKOUT_TEMPLATE = os.path.join(BASE_DIR, 'main\\templates\\main\\lockout.html')
#DEFENDER_LOCK_OUT_BY_IP_AND_USERNAME = True
#DEFENDER_DISABLE_USERNAME_LOCKOUT = True

# Login
LOGIN_REDIRECT_URL = 'profile_redirect'
LOGIN_URL = 'login'

# Recaptcha
RECAPTCHA_PUBLIC_KEY = config['RECAPTCHA_PUBLIC_KEY']
RECAPTCHA_PRIVATE_KEY = config['RECAPTCHA_PRIVATE_KEY']

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'main/static'),
    #BASE_DIR / "static",
]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Media
MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Crispy forms
CRISPY_TEMPLATE_PACK = 'bootstrap4'

# Email settings

EMAIL_HOST = 'smtp.gmail.com' 
EMAIL_HOST_USER =  config['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = config['EMAIL_HOST_PASSWORD']
EMAIL_PORT = 587 
EMAIL_USE_TLS = True 
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'


#Ckeditor
CKEDITOR_CONFIGS = {
    'default': {
        'codeSnippet_theme': 'monokai_sublime',
        'toolbar_Full': [
            ['Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord'], 
            ['Preview', 'Templates'],
            ['Find', 'Replace', 'SelectAll', 'Scayt'],
            ['Link', 'Unlink', 'Anchor'], ['EmojiPanel', 'SpecialChar'],
            ['Image', 'Youtube', 'CodeSnippet', 'Table', 'HorizontalRule'],  
            ['Bold', 'Italic', 'Underline', 'Strike'], ['Subscript', 'Superscript'], ['CopyFormatting', 'RemoveFormat'],
            ['TextColor', 'BGColor'],
            ['NumberedList', 'BulletedList'], ['Outdent', 'Indent'],  
            ['JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'], ['BidiLtr', 'BidiRtl'],
            ['Styles'], ['Format'], ['Font'], ['FontSize'], ['Undo', 'Redo'],
        ],
        'extraPlugins': 'justify,liststyle,indent,codesnippet,emoji,autocomplete,textmatch,textwatcher,youtube',
        'height': 380,
        'width': '100%',
        'startupFocus' : True,
        'youtube_responsive': True,
    },
}

CKEDITOR_UPLOAD_PATH = 'uploads/'

#Messages styles
MESSAGE_TAGS = {
    messages.DEBUG: 'info',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'danger',
}

