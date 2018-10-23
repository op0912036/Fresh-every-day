# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0002_auto_20181016_2200'),
    ]

    operations = [
        migrations.CreateModel(
            name='IndexGoodsBanner',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('create_time', models.DateTimeField(verbose_name='创建时间', auto_now_add=True)),
                ('update_time', models.DateTimeField(verbose_name='更新时间', auto_now=True)),
                ('is_delete', models.BooleanField(verbose_name='删除标记', default=False)),
                ('image', models.ImageField(verbose_name='图片', upload_to='banner')),
                ('index', models.SmallIntegerField(verbose_name='展示顺序', default=1)),
                ('sku', models.ForeignKey(verbose_name='商品', to='goods.GoodsSKU')),
            ],
            options={
                'verbose_name': '首页轮播商品',
                'verbose_name_plural': '首页轮播商品',
                'db_table': 'fed_index_banner',
            },
        ),
        migrations.CreateModel(
            name='IndexPromotionBanner',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('create_time', models.DateTimeField(verbose_name='创建时间', auto_now_add=True)),
                ('update_time', models.DateTimeField(verbose_name='更新时间', auto_now=True)),
                ('is_delete', models.BooleanField(verbose_name='删除标记', default=False)),
                ('name', models.CharField(max_length=20, verbose_name='活动名称')),
                ('url', models.CharField(max_length=256, verbose_name='活动链接')),
                ('image', models.ImageField(verbose_name='活动图片', upload_to='banner')),
                ('index', models.SmallIntegerField(verbose_name='展示顺序', default=1)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='IndexTypeGoodsBanner',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('create_time', models.DateTimeField(verbose_name='创建时间', auto_now_add=True)),
                ('update_time', models.DateTimeField(verbose_name='更新时间', auto_now=True)),
                ('is_delete', models.BooleanField(verbose_name='删除标记', default=False)),
                ('display_type', models.SmallIntegerField(verbose_name='展示方式', choices=[(0, '标题'), (1, '图片')], default=1)),
                ('index', models.SmallIntegerField(verbose_name='展示顺序', default=1)),
                ('sku', models.ForeignKey(verbose_name='商品SKU', to='goods.GoodsSKU')),
                ('type', models.ForeignKey(verbose_name='商品类型', to='goods.GoodsType')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
