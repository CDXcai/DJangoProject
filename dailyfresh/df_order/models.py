#coding:utf8
from django.db import models

# Create your models here.
class order_info(models.Model):
    # 关联到用户表，表示哪个用户的订单
    user = models.ForeignKey('df_user.UserInfo')
    # 用户支付的时间
    odate = models.DateField(auto_now=True)
    # 订单的总价,总位数6位，包含两位小数
    otatal = models.DecimalField(max_digits=6,decimal_places=2)
    # 是否支付成功
    oispay = models.BooleanField(default=False)
    # 订单的地址
    oaddress = models.CharField(max_length=100)


# 订单的详细内容
class order_detail_info(models.Model):
    # 购买的商品
    goods = models.ForeignKey('df_goods.GoodsInfo')
    # 购买的数量
    count = models.IntegerField()
    # 属于哪个订单
    order = models.ForeignKey(order_info)
    # 商品的单价
    price = models.DecimalField(max_digits=5,decimal_places=2)