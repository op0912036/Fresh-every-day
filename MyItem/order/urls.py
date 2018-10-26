from django.conf.urls import include, url
from order import views

urlpatterns = [
    # 提交订单页面显示
    url(r'^place$', views.OrderPlaceView.as_view(), name='place'),
    # 订单创建
    url(r'^commit$', views.OrderCommitView.as_view(), name='commit'),
]
