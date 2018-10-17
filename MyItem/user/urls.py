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
    # 登出
    url(r'^logout$', views.LogoutView.as_view(), name='logout'),

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

    # 三级联动-省
    url(r'^get_all_province$', views.get_all_province, name='get_all_province'),
    # 三级联动-市
    url(r'^get_city_by_province_code$', views.get_city_by_province_code, name='get_city_by_province_code'),
    # 三级联动-区/县
    url(r'^get_town_by_city_code$', views.get_town_by_city_code, name='get_town_by_city_code'),
]
