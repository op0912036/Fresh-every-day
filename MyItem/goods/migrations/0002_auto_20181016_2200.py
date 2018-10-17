# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goodssku',
            name='status',
            field=models.SmallIntegerField(default=1, choices=[(0, '下线'), (1, '上线')], verbose_name='商品状态'),
        ),
    ]
