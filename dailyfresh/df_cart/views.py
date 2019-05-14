# coding:utf8
from django.shortcuts import render,redirect
from django.http import JsonResponse

from .models import *
from df_user.models import *
from df_goods.models import *

from df_user.user_mod import *
# Create your views here.
# 验证是否登录
@user_verification_login
def cart(request):
    # 查找用户购买的商品
    # 读取用户登录信息
    user = request.session.get('username')
    # 查找用户id
    uid = UserInfo.objects.filter(uname=user)[0].id
    # 查找用户购买的所有商品记录
    cart_list = CartInfo.objects.filter(user_id = int(uid))
    # print len(cart_list)
    goods_list = []
    for i in cart_list[::-1]:
        # i为商品记录 GoodsInfo.objects.filter(id = i.goods_id)[0]为记录对应的商品对象
        goods_list.append([i,GoodsInfo.objects.filter(id = i.goods_id)[0]])
    content = {
        'cart':goods_list,
    }
    request.session['shopping'] = len(cart_list)
    return render(request,'df_cart/cart.html',content)




# 验证是否登录
@user_verification_login
def add_cart_handle(request,cid,cnum):
    # 商品的id
    id = int(cid)
    # 商品的数量
    num = int(cnum)
    # 读取用户登录信息
    user = request.session.get('username')
    # 查找用户id
    uid = UserInfo.objects.filter(uname=user)[0].id
    # 判断用户的购物车是否有同样的商品
    goods_cart = CartInfo.objects.filter(user_id = int(uid),goods_id=id)
    if len(goods_cart) > 0:
        # 如果之前有同样的商品购买记录，则在原来的数量上加num
        cart = goods_cart[0]
        cart.count += num
    else:
        # 如果没有同样的商品购买几率，则创建对象
        cart = CartInfo()
        cart.user_id = int(uid)
        cart.goods_id = id
        cart.count = num
    # 保存数据
    cart.save()

    # print user,uid

    # 判断是否是Ajax发出的请求
    if request.is_ajax():
        # 如果是ajax请求，则返回数量
        return JsonResponse({'count':cart.count,
                             'cart_list':len(CartInfo.objects.filter(user_id = int(uid)))})
    else:
        # 如果不是ajax发送的请求，则重定向到购物车
        return redirect('/cart/')

# 修改购物车
def remove_item(request,uid,gid):
    CartInfo.objects.filter(user_id = uid,goods_id = gid).delete()
    return JsonResponse({'True':'true'})


#修改商品的数量
def update_item(request,uid,gid,num):
    #查找到指定商品
    item = CartInfo.objects.filter(user_id=uid, goods_id=gid)[0]
    item.count = int(num)
    item.save()
    return JsonResponse({'True':'true'})