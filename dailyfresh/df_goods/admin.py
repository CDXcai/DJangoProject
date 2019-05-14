# coding:utf8
from django.contrib import admin
from .models import *

# typeinfo管理类
class TypeInfoAdmin(admin.ModelAdmin):
    # 决定要在admin管理页面显示的字段
    list_display = ['id','ttitle']
# GoodsInfo管理类
class GoodsInfoAdmin(admin.ModelAdmin):
    list_display = ['id','gtitle','gprice','gcompany','gclick','gstock']

# 向admin中注册管理类
admin.site.register(TypeInfo,TypeInfoAdmin)
admin.site.register(GoodsInfo,GoodsInfoAdmin)

