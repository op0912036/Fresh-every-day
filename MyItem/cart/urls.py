from django.conf.urls import include, url
from cart import views

urlpatterns = [
    # 购物车记录添加
    url(r'^add$', views.CartAddView.as_view(), name='add'),
]
