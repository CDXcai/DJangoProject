# coding:utf8
from django.db import models


class CartInfo(models.Model):
    # 购买的用户,引用其他应用的模型类直接 (应用.模型类名称)
    user = models.ForeignKey('df_user.UserInfo')
    # 购买的商品
    goods = models.ForeignKey('df_goods.GoodsInfo')
    # 购买的数量
    count = models.IntegerField()
