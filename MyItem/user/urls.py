from django.conf.urls import include, url
from user import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    # 注册
    url(r'^register$', views.RegisterView.as_view(), name='register'),
    # 用户激活
    url(r'^active/(?P<token>.*)$', views.ActiveView.as_view(), name='active'),
    # 登录
    url(r'^login$', views.LoginView.as_view(), name='login'),
    # 验证码
    url(r'^validate_code$', views.validate_code, name='validate_code'),
    # 异步验证用户名是否存在
    url(r'^checkusername$', views.checkusername, name='checkusername'),

    # 用户中心-信息页
    url(r'^$', views.UserInfoView.as_view(), name='user'),
    # 用户中心-订单页
    url(r'^order$', views.UserOrderView.as_view(), name='order'),
    # 用户中心-地址页
    url(r'^address$', views.UserAddressView.as_view(), name='address'),
]
