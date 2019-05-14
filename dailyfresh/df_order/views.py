#coding:utf8
from django.shortcuts import render
from django.http import JsonResponse
from df_user.user_mod import *
from df_user.models import *
from df_cart.models import *
from df_goods.models import *
from models import *
from django.views.decorators.csrf import csrf_exempt
import time
# Create your views here.
@user_verification_login
def order(request):
    # 获取商品id列表
    a = request.GET.getlist('goods_id')
    # 获取商品数量列表
    b = request.GET.getlist('goos_count')
    # 获取商品总价
    sum = '%.2f'%(float(request.GET.get('sum')))

    goods_object = []

    for i in range(len(a)):
        # 获取商品对象
        goods = GoodsInfo.objects.get(id = a[i])
        # 添加 商品对象 和 商品数量 到列表
        goods_object.append([goods,b[i]])


    context = {
        'goods':goods_object,
        'sum':sum,
    }



    return render(request,'df_order/place_order.html',context)

@csrf_exempt
def handle(request):
    # 获取商品id列表
    a = request.POST['id'].split('-')
    # 获取商品数量列表
    b = request.POST['count'].split('-')
    # 获取商品总价
    sum = request.POST['sum']

    #读取用户登录信息
    user = request.session.get('username')
    # 根据用户登录情况查找用户对象
    user_ob = UserInfo.objects.get(uname=user)

    # 创建用户的订单读表
    orderInfo = order_info()

    # 写入数据内容
    # 关联用户对象
    orderInfo.user = user_ob
    # 订单总价
    orderInfo.otatal = float(sum)
    # # 订单地址
    address = user_ob.uaddress + ' ('+ user_ob.urecipient +') ' + user_ob.uphone
    orderInfo.oaddress = address
    # 保存数据
    orderInfo.save()
    #遍历a列表即可获取所有选中的商品
    for i in range(0,len(a)):
        # 获取商品对象
        goods = GoodsInfo.objects.get(id = int(a[i]))
        # 创建订单的详细内容
        goods_datil = order_detail_info()
        # 关联订单读表
        goods_datil.order = orderInfo
        # 商品单价
        goods_datil.price = goods.gprice
        # 关联商品对象
        goods_datil.goods = goods
        # 商品购买的数量
        goods_datil.count = int(b[i])
        # 保存数据
        goods_datil.save()
        # 删除购物车
        c = CartInfo.objects.get(goods_id=int(a[i]), user_id=user_ob.id)
        c.delete()

    time.sleep(2000)
    return JsonResponse({'True': 'true'})