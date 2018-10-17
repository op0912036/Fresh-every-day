from django.db import models
from django.contrib.auth.models import AbstractUser
from db.base_model import BaseModel


class User(AbstractUser, BaseModel):
    '''用户 模型类'''

    class Meta:
        db_table = 'fed_user'
        verbose_name = '用户'
        verbose_name_plural = verbose_name


class Address(BaseModel):
    '''地址 模型类'''
    user = models.ForeignKey('user', verbose_name='所属账户')
    receiver = models.CharField(max_length=20, verbose_name='收件人')
    addr = models.CharField(max_length=256, verbose_name='收件人地址')
    zip_code = models.CharField(max_length=6, null=True, verbose_name='邮政编码')
    phone = models.CharField(max_length=11, verbose_name='联系电话')
    is_default = models.BooleanField(default=False, verbose_name='是否默认')

    class Meta:
        db_table = 'fed_address'
        verbose_name = '地址'
        verbose_name_plural = verbose_name


class Province(models.Model):
    '''三级联动-省 模型类'''
    code = models.CharField(max_length=6)
    name = models.CharField(max_length=40)

    class Meta:
        db_table = 'fed_address_province'
        verbose_name = '三级联动-省'
        verbose_name_plural = verbose_name


class City(models.Model):
    '''三级联动-市 模型类'''
    code = models.CharField(max_length=6)
    name = models.CharField(max_length=40)
    province_code = models.CharField(db_column='provinceCode', max_length=6)

    class Meta:
        db_table = 'fed_address_city'
        verbose_name = '三级联动-市'
        verbose_name_plural = verbose_name


class Town(models.Model):
    '''三级联动-区/县 模型类'''
    code = models.CharField(max_length=6)
    name = models.CharField(max_length=40)
    city_code = models.CharField(db_column='cityCode', max_length=6)

    class Meta:
        db_table = 'fed_address_town'
        verbose_name = '三级联动-区/县'
        verbose_name_plural = verbose_name
