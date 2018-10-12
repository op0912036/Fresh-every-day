from django.conf.urls import include, url
from django.contrib import admin
from user import views

urlpatterns = [
    # 注册
    url(r'^register$', views.RegisterView.as_view(), name='register'),
    # 用户激活
    url(r'^active/(?P<token>.*)$', views.ActiveView.as_view(), name='active'),
    # 登录
    url(r'^login$', views.LoginView.as_view(), name='login'),
]
