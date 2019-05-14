# coding:utf8

from django.db import models

# Create your models here.
class UserInfo(models.Model):
    # 用户名
    uname = models.CharField(max_length=20)
    # 密码
    upwd = models.CharField(max_length=40)
    # 邮箱
    uemil = models.CharField(max_length=30)
    # 收货人名字
    urecipient = models.CharField(max_length=20,default='')
    # 收货地址
    uaddress = models.CharField(max_length=100,default='')
    # 邮编
    ucode = models.CharField(max_length=7,default='')
    # 电话号码
    uphone = models.CharField(max_length=11,default='')