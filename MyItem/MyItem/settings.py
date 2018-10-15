"""
Django settings for MyItem project.
Generated by 'django-admin startproject' using Django 1.8.2.
For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/
For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '5%#ko-4+_40r82o+4pjlglbr0xkn_vhpp2bo0$q)gjde1o^r#p'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

# 配置APP
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'user',
    'goods',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'MyItem.urls'

# 配置模板
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'MyItem.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases


# 配置连接mysql数据库
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': '192.168.12.193',
        'PORT': '3306',
        'NAME': 'FreshEveryDay',
        'USER': 'root',
        'PASSWORD': '55555',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

# 配置时区
LANGUAGE_CODE = 'zh-Hans'

# 配置语言
TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# 设置字体
FONT_STYLE = '/usr/share/fonts/truetype/freefont/FreeMono.ttf'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

# 配置静态文件
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# session交给redis管理
SESSION_ENGINE = 'redis_sessions.session'
SESSION_REDIS_HOST = '192.168.12.193'
SESSION_REDIS_PORT = 6379
SESSION_REDIS_DB = 1
SESSION_REDIS_PASSWORD = ''
SESSION_REDIS_PREFIX = 'session'

# 配置django认证系统使用的模型类
AUTH_USER_MODEL = 'user.User'

# 配置发送邮件
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.126.com'  # SMTP服务器
EMAIL_POST = 25  # 端口号
EMAIL_HOST_USER = 'op0912036@126.com'  # 发送邮件的邮箱
EMAIL_HOST_PASSWORD = '6190543y'  # 邮箱的授权码（不是登陆密码）
EMAIL_FROM = '天天生鲜<op0912036@126.com>'

# 配置登录url
LOGIN_URL = '/user/login'
