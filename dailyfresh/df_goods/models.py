# coding:utf8
from django.db import models
from tinymce.models import HTMLField

class TypeInfo(models.Model):
    ttitle = models.CharField(max_length=20)
    isDelete = models.BooleanField(default=False)
    def __str__(self):
        return self.ttitle.encode('utf-8')


class GoodsInfo(models.Model):
    # 商品名称
    gtitle = models.CharField(max_length=20)
    # 商品图片
    gimage = models.ImageField(upload_to='df_goods')
    # 商品价格
    gprice = models.DecimalField(max_digits=10,decimal_places=2)
    # 商品单位
    gcompany = models.CharField(max_length=20)
    # 逻辑删除
    isDelete = models.BooleanField(default=False)
    # 点击量(人气)
    gclick = models.IntegerField()
    # 库存
    gstock = models.IntegerField()
    # 简介
    gbi = models.CharField(max_length=20)
    # 详细介绍
    gcontent = HTMLField()
    # 关联对象
    gtype = models.ForeignKey(TypeInfo)
