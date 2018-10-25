from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse
from django.conf import settings
from goods.models import *


# Create your views here.
class CartAddView(View):
    '''购物车添加记录'''

    def post(self, request):
        user = request.user
        if not user.is_authenticated():
            # 用户为登录
            return JsonResponse({'res': 0, 'errmsg': '请先登录'})

        # 接收数据
        sku_id = request.POST.get('sku_id')
        count = request.POST.get('count')

        # 数据校验
        if not all([sku_id, count]):
            return JsonResponse({'res': 1, 'errmsg': '数据不完整'})

        # 校验添加的商品数量
        try:
            count = int(count)
        except Exception:
            # 数目出错
            return JsonResponse({'res': 2, 'errmsg': '商品数目出错'})

        # 校验商品是否存在
        try:
            sku = GoodsSKU.objects.get(id=sku_id)
        except GoodsSKU.DoesNotExist:
            # 商品不存在
            return JsonResponse({'res': 3, 'errmsg': '商品不存在'})

        # 业务处理：添加购物车记录
        conn = settings.REDIS_CONN
        cart_key = 'cart_%d' % user.id
        # 先尝试获取sku_id的值 -> hget cart_key 属性
        # 如果sku_id在hash中不存在，hget返回None
        cart_count = conn.hget(cart_key, sku_id)
        if cart_count:
            # 累加购物车中商品的数目
            count += int(cart_count)

        # 校验商品的库存
        if count > sku.stock:
            return JsonResponse({'res': 4, 'errmsg': '商品库存不足'})

        # 设置hash中sku_id对应的值
        # hset -> 如果sku_id已经存在，更新数据，如果sku_id不存在，添加数据
        conn.hset(cart_key, sku_id, count)

        # 计算用户购物车商品的条目数
        total_count = get_cart_count(user)

        # 返回应答
        return JsonResponse({'res': 5, 'total_count': total_count, 'message': '添加成功'})


def get_cart_count(user):
    '''获取用户的购物车购买商品的总数'''

    # 保存用户购物车中商品的总数目
    total_count = 0

    if user.is_authenticated():
        # 连接redis
        conn = settings.REDIS_CONN
        # key
        cart_key = 'cart_%d' % user.id
        # 获取信息
        cart_dict = conn.hgetall(cart_key)

        # 遍历获取商品的信息
        for sku_id, count in cart_dict.items():
            total_count += int(count)

    return total_count
