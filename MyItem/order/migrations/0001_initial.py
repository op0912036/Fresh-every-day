# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0004_auto_20181022_2024'),
        ('user', '0004_auto_20181017_1902'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderGoods',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='删除标记')),
                ('count', models.IntegerField(default=1, verbose_name='商品数目')),
                ('price', models.DecimalField(decimal_places=2, verbose_name='商品价格', max_digits=10)),
            ],
            options={
                'verbose_name': '订单商品',
                'verbose_name_plural': '订单商品',
                'db_table': 'fed_order_goods',
            },
        ),
        migrations.CreateModel(
            name='OrderInfo',
            fields=[
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='删除标记')),
                ('order_id', models.CharField(max_length=128, serialize=False, primary_key=True, verbose_name='订单id')),
                ('pay_method', models.SmallIntegerField(default=3, verbose_name='支付方式', choices=[(2, '微信支付'), (1, '货到付款'), (4, '银联支付'), (3, '支付宝')])),
                ('total_count', models.IntegerField(default=1, verbose_name='商品数量')),
                ('total_price', models.DecimalField(decimal_places=2, verbose_name='商品总价', max_digits=10)),
                ('transit_price', models.DecimalField(decimal_places=2, verbose_name='订单运费', max_digits=10)),
                ('order_status', models.SmallIntegerField(default=1, verbose_name='订单状态', choices=[(4, '待评价'), (3, '待收货'), (5, '已完成'), (1, '待支付'), (2, '待发货')])),
                ('trade_no', models.CharField(max_length=128, default='', verbose_name='支付编号')),
                ('addr', models.ForeignKey(verbose_name='地址', to='user.Address')),
                ('user', models.ForeignKey(verbose_name='用户', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '订单',
                'verbose_name_plural': '订单',
                'db_table': 'fed_order_info',
            },
        ),
        migrations.AddField(
            model_name='ordergoods',
            name='order',
            field=models.ForeignKey(verbose_name='订单', to='order.OrderInfo'),
        ),
        migrations.AddField(
            model_name='ordergoods',
            name='sku',
            field=models.ForeignKey(verbose_name='商品SKU', to='goods.GoodsSKU'),
        ),
    ]
