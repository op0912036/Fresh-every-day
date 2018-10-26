from django.conf.urls import include, url
from cart import views

urlpatterns = [
    # 购物车记录添加
    url(r'^add$', views.CartAddView.as_view(), name='add'),
    # 异步获取购物车总数量
    url(r'^count$', views.CartCountView.as_view(), name='count'),
    # 购物车页面显示
    url(r'^info$', views.CartInfoView.as_view(), name='info'),
    # 购物车记录更新
    url(r'^update$', views.CartUpdateView.as_view(), name='update'),
    # 购物车记录删除
    url(r'^delete$', views.CartDeleteView.as_view(), name='delete'),
]
