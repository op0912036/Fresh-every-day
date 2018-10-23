# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0003_indexgoodsbanner_indexpromotionbanner_indextypegoodsbanner'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='indexgoodsbanner',
            options={'verbose_name': '主页轮播商品', 'verbose_name_plural': '主页轮播商品'},
        ),
        migrations.AlterModelOptions(
            name='indexpromotionbanner',
            options={'verbose_name': '主页促销活动', 'verbose_name_plural': '主页促销活动'},
        ),
        migrations.AlterModelOptions(
            name='indextypegoodsbanner',
            options={'verbose_name': '主页分类展示商品', 'verbose_name_plural': '主页分类展示商品'},
        ),
        migrations.AlterModelTable(
            name='indexpromotionbanner',
            table='fed_index_promotion',
        ),
        migrations.AlterModelTable(
            name='indextypegoodsbanner',
            table='fed_index_type_goods',
        ),
    ]
