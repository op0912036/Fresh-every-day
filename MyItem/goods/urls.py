from django.conf.urls import include, url
from goods import views

urlpatterns = [
    # 主页
    url(r'^index$', views.IndexView.as_view(), name='index'),
    url(r'^$', views.IndexView.as_view(), name='index'),

    # 详情页面
    url(r'^goods/(?P<goods_id>\d+)$', views.DetailView.as_view(), name='detail'),
]
