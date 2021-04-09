"""
Django settings for gaoxiaoyq project.

Generated by 'django-admin startproject' using Django 2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ki9jt3-koaunp8wb0$3lkb0-yse)8o(dz1+u1+8sa(cuuy7ev!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# jwt的过期时间 以及 jwt的前缀
import datetime

JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=7),  # 设置 JWT Token 的有效时间
    'JWT_AUTH_HEADER_PREFIX': 'JWT',  # 设置 请求头中的前缀
}


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'hot_news',
    'corsheaders',
    'user_profile',
    'rest_framework',
    'rest_framework.authtoken'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # 跨域问题
    'django.middleware.common.CommonMiddleware',
    # csrf
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# 跨域增加忽略
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True
# CORS_ORIGIN_WHITELIST = (
#   "*"
# )

CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
    'VIEW',
)

# 允许所有的请求头
CORS_ALLOW_HEADERS = (
    'XMLHttpRequest',
    'X_FILENAME',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
)

ROOT_URLCONF = 'gaoxiaoyq.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'frontend')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'gaoxiaoyq.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': "gaoxiao_back",
        'USER': "root",
        "PASSWORD": "209243",
        "HOST": "127.0.0.1",
        "PORT": "3306",
        'OPTIONS': {
            'charset': 'utf8mb4'
        }
    },
    # 'spider': {
    #     'ENGINE': 'django.db.backends.mysql',
    #     'NAME': "gaoxiaoYQ",
    #     'USER': "root",
    #     "PASSWORD": "209243",
    #     "HOST": "127.0.0.1",
    #     "PORT": "3306",
    #     'OPTIONS': {
    #         'charset': 'utf8mb4'
    #     }
    # },
}

# spider 数据库


# DATABASE_ROUTERS = ['gaoxiaoyq.database_app_router.DatabaseAppsRouter']
#
# DATABASES_APPS_MAPPING = {
#     'user_profile': 'default',
#     'hot_news': 'spider'
# }

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/
from rest_framework_jwt.authentication import JSONWebTokenAuthentication


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True


# USE_TZ = True


# 重写 去掉csrf
class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening


# authentication_classes = ()


# 使用[] 则没有权限
# 使用SessionAuthentication才可以使用request.user
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        # 'rest_framework.permissions.AllowAny',
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        # 'rest_framework.authentication.TokenAuthentication'
        # 'rest_framework.authentication.SessionAuthentication',
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    )
}




STATIC_URL = '/static/'


## python manage.py collectstatic时，把所有静态文件聚集到此目录下
STATIC_ROOT = os.path.join(BASE_DIR, 'frontend/static')

## 访问 http://IP/media/***.file
MEDIA_URL = '/media/'

## 用户上传文件的存放目录
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# 发送邮件

EMAIL_BACKEMD = 'django.core.mail.backends.smtp.EmailBackend'
# 是否使用 TLS
EMAIL_USE_TLS = True
# SMTP服务器，改为你的邮箱的smtp!
EMAIL_HOST = 'smtp.qq.com'
# 改为你自己的邮箱名！
EMAIL_HOST_USER = '209243446@qq.com'
# 你的邮箱密码
EMAIL_HOST_PASSWORD = 'fqzuqwrmeodjcbbf'
# 发送邮件的端口
EMAIL_PORT = 25

EMIAL_USE_TLS = False

EMAIL_SUBJECT_PREFIX = u'[Sercheif]'


# EMAIL_FROM = "博客yanzx@163.com"
# 默认的发件人
DEFAULT_FROM_EMAIL = '209243446@qq.com'


CRAWL_HEADERS = {
    'User-Agent': "Mozilla/5.0 (Linux; U; Android 2.3.6; en-us; Nexus S Build/GRK39F) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

# DRF扩展
REST_FRAMEWORK_EXTENSIONS = {
    # 缓存时间
    'DEFAULT_CACHE_RESPONSE_TIMEOUT': 60 * 60,
    # 缓存存储
    'DEFAULT_USE_CACHE': 'default',
}
