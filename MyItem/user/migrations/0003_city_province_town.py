# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_address'),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('code', models.CharField(max_length=6)),
                ('name', models.CharField(max_length=40)),
                ('provin_cecode', models.CharField(db_column='provinceCode', max_length=6)),
            ],
            options={
                'verbose_name_plural': '三级联动-市',
                'verbose_name': '三级联动-市',
                'db_table': 'fed_address_city',
            },
        ),
        migrations.CreateModel(
            name='Province',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('code', models.CharField(max_length=6)),
                ('name', models.CharField(max_length=40)),
            ],
            options={
                'verbose_name_plural': '三级联动-省',
                'verbose_name': '三级联动-省',
                'db_table': 'fed_address_province',
            },
        ),
        migrations.CreateModel(
            name='Town',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('code', models.CharField(max_length=6)),
                ('name', models.CharField(max_length=40)),
                ('city_code', models.CharField(db_column='cityCode', max_length=6)),
            ],
            options={
                'verbose_name_plural': '三级联动-区/县',
                'verbose_name': '三级联动-区/县',
                'db_table': 'fed_address_town',
            },
        ),
    ]
