#coding:utf8
from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from . import models

from hashlib import sha1
from user_mod import *
from df_cart.models import *
from df_user.models import UserInfo
from df_order.models import order_info

from django.core.paginator import Paginator
import time
import sys
sys.path.append('..')

'''导入其他模型类'''
from df_goods.models import GoodsInfo
from df_user.models import *

# Create your views here.
# sha1加密
def sha1_pwd(con):
    s1 = sha1()
    s1.update(con)
    return s1.hexdigest()
# 显示注册页面
def register(request):

    return render(request,'df_user/register.html')
# 处理注册页面提交的表单
def registerHandle(request):
    # 接受表单提交的内容
    post = request.POST
    uname = post.get('user_name')
    upwd = post.get('pwd')
    uemail = post.get('email')
    # 查询是否有相同的用户名
    count = UserInfo.objects.filter(uname = uname).count()
    if count == 0:
        user = UserInfo()
        user.uname = uname
        user.upwd = sha1_pwd(upwd)
        user.uemil = uemail
        user.save()
    else:
        # 如果用户名存在，则重新到注册页面
        return redirect('/user/register/')
    # 注册成功，重定向到登录页面
    return redirect('/user/login/')
# 判断用户名是否存在
def register_exits(request):
    uname = request.GET.get('uname')

    count = models.UserInfo.objects.filter(uname = uname).count()
    return JsonResponse({'count':count})
# 显示登录页面
def login(request):
    # 获取用户名
    uname = request.COOKIES.get('uname','')


    return render(request,'df_user/login.html',{'uname':uname})
def loginhandle(request):
    uname = request.GET.get('name')
    count = UserInfo.objects.filter(uname = uname).count()
    return JsonResponse({'count':count})

def loginhandlepwd(request):
    uname = request.GET.get('uname')
    upwd = request.GET.get('upwd')
    list = UserInfo.objects.filter(uname = uname)
    # print uname,upwd
    # print list[0].upwd,upwd
    if list[0].upwd == sha1_pwd(upwd):
        count = 0
    else:
        count = 1
    return JsonResponse({'count':count})
def loginSubmission(request):
    upwd = request.POST.get('pwd','0')

    # 查询是否有记录的url信息,如果没有则重定向到首页
    lurl = request.COOKIES.get('url','/')
    red = redirect(lurl)
    print upwd
    if upwd == '1':
        # 如果用户勾选了记住用户名，则设置cookie,过期时间6天
        # print request.POST.get('username')
        red.set_cookie('uname',request.POST.get('username'),max_age=60*60*12*6)
    else:
        # 没有勾选记住用户名，则设置空cookie，并立即过过期
        red.set_cookie('uname','',max_age=-1)
    # 设置session,保持登录状态
    request.session['username'] = request.POST.get('username')
    # 设置过期时间
    request.session.set_expiry(0)
    return red

# 处理用户中心页面
@user_verification_login
def info(request):
    # 查询登录状态
    uname = request.session.get('username')

    # 获取用户信息
    user = UserInfo()
    uphone = user.uphone
    uaddress = user.uaddress

    # print uphone,uaddress

    # 读取最近浏览的商品
    goods = request.COOKIES.get('goods_ids', '')
    goods_L = []
    # 如果读取到了内容
    if goods != '':
        # 拆分字符串
        goodslist = goods.split(',')
        print goodslist
        # 依次读取
        for id in goodslist:
            if id != '':
                goods_L.append(GoodsInfo.objects.get(id=int(id)))

    context = {
        'uname': uname,
        'uphone': uphone,
        'uaddress': uaddress,
        'goodslist':goods_L,
    }
    return render(request,'df_user/user_center_info.html',context)

# 处理管理地址页面
@user_verification_login
def site(request):
    # 查询登录状态
    uname = request.session.get('username')
    # 获取用户信息
    user = UserInfo.objects.get(uname = uname)
    uaddress = user.uaddress
    uemail = user.uemil
    uphone = user.uphone
    urecipient = user.urecipient
    context = {
        'uname':uname,
        'uaddress':uaddress,
        'uemail':uemail,
        'uphone':uphone,
        'uphone1':uphone[0:3],
        'uphone2':uphone[-4:],
        'urecipient':urecipient

    }

    return render(request,'df_user/user_center_site.html',context)
# 处理收货地址表单
@user_verification_login
def sitehandle(request):
    # 接受收货人信息
    uname = request.session.get('username')
    urecipient = request.POST.get('urecipient')
    uaddress = request.POST.get('uaddress')
    ucode = request.POST.get('ucode')
    uphone = request.POST.get('uphone')
    # 保存收货人信息
    user = UserInfo.objects.get(uname=uname)
    user.urecipient = urecipient
    user.uaddress = uaddress
    user.ucode = ucode
    user.uphone = uphone
    user.save()

    return redirect('/user/site/')
@user_verification_login
def order(request,pindex):
    # 查找用户名
    user = request.session.get('username')
    # 查找用户对象
    user_ob = UserInfo.objects.get(uname = user)
    # 根据用户查找所有的订单
    order = order_info.objects.filter(user_id = user_ob.id)


    # 遍历order构造数据
    content = []
    for i in order:
        j = []
        # 获取订单详情列表
        orderInfo = i.order_detail_info_set.all()
        # print orderInfo
        for x in orderInfo:
            j.append([x,GoodsInfo.objects.get(id = x.goods_id)])
        content.append([i,j])

    # 获取订单数量
    goods_count = len(order)

    # 分页功能
    # 判断是否有参数，如果没有参数默认为第一页
    if pindex == '':
        pindex = 1
    # 转化为数字类型
    pindex = int(pindex)
    # 创建分页对象,五个订单为一页
    p = Paginator(content[::-1],3)
    plist = p.page(pindex)
    previndex = pindex - 1
    nextindex = pindex + 1
    context = {
        'content':plist,
        'pindex':p.page_range,
        'index':pindex,
        'previndex':previndex,
        'nextindex':nextindex,
        'len':len(p.page_range),
        'gooss_count':goods_count,
    }
    return render(request,'df_user/user_center_order.html',context)

def logout(request):
    # 清空session
    request.session.flush()
    return HttpResponseRedirect('/')

# 返回购物车的数量
def car_len(request):
    # 查找用户购买商品的数量
    uname = request.session.get('username')
    CartList = 0
    if uname != None:
        print uname
        # 根据用户名称查找用户id
        User_id = UserInfo.objects.get(uname=uname).id
        # 查找购物车商品的数量
        CartList = len(CartInfo.objects.filter(user_id=User_id))
        print CartList
    return JsonResponse({'carlen':CartList})