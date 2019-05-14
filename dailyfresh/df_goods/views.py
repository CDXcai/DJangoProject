# coding:utf8
from django.shortcuts import render
from .models import *
from django.core.paginator import *
from df_cart.models import *
from df_user.models import *
# insert into df_goods_typeinfo value('海鲜水产','0');
def index(request):

    # 查找所有的类型
    typelist = TypeInfo.objects.all()

    # 根据类型查找类型下的商品
    """
    测试代码，实际运行代码应该为
    goodlist0 = typelist[0].goodsinfo_set.order_by('-id')[0:4]
    """
    goodlist0 = typelist[0].goodsinfo_set.order_by('-id')[0:4]#根据id排序,-为倒序
    goodlist1 = typelist[1].goodsinfo_set.order_by('-id')[0:4]
    goodlist2 = typelist[2].goodsinfo_set.order_by('-id')[0:4]
    goodlist3 = typelist[3].goodsinfo_set.order_by('-id')[0:4]
    goodlist4 = typelist[4].goodsinfo_set.order_by('-id')[0:4]
    goodlist5 = typelist[5].goodsinfo_set.order_by('-id')[0:4]
    goodlist01 = typelist[0].goodsinfo_set.order_by('gclick')[0:4] # 根据点击量排序,-为倒序
    goodlist11 = typelist[1].goodsinfo_set.order_by('gclick')[0:4]
    goodlist21 = typelist[2].goodsinfo_set.order_by('gclick')[0:4]
    goodlist31 = typelist[3].goodsinfo_set.order_by('gclick')[0:4]
    goodlist41 = typelist[4].goodsinfo_set.order_by('gclick')[0:4]
    goodlist51 = typelist[5].goodsinfo_set.order_by('gclick')[0:4]


    # 查找用户购买商品的数量
    uname = request.session.get('username')
    CartList = 0
    if uname != None:
        # 根据用户名称查找用户id
        User_id = UserInfo.objects.get(uname = uname).id
        # 查找购物车商品的数量
        CartList = len(CartInfo.objects.filter(user_id = User_id))
        # print CartList





    content = {
        'g0':goodlist0,
        'g01': goodlist01,
        'g1': goodlist1,
        'g11': goodlist11,
        'g2': goodlist2,
        'g21': goodlist21,
        'g3': goodlist3,
        'g31': goodlist31,
        'g4': goodlist4,
        'g41': goodlist41,
        'g5': goodlist5,
        'g51': goodlist51,
        'list':[0,1,2,3],
        'uname':uname,
        'cartlen':CartList,
    }

    return render(request,'df_goods/index.html',content)

# 返回list.html，参数分别为  要查找的商品的类型id  分页数据的第几页  排序的规则(id、价格、人气)
def list(request,tid,tindex,tclick):
    # 返回符合商品id的typeinfo对象
    typelist = TypeInfo.objects.filter(id = int(tid))[0]
    # print typelist,int(tid)
    # 判断应该用哪种方式排序
    if tclick == '1':
        # 根据typeinfo对象查找到所有的关联数据
        goodslist = typelist.goodsinfo_set.order_by('id')
        """
        实际运行代码应为
        goodslist = typelist.goodsinfo_set.order_by('id')
        """
    elif tclick == '2':
        goodslist = typelist.goodsinfo_set.order_by('gprice')
        """
        实际运行代码应为
        goodslist = typelist.goodsinfo_set.order_by('gprice')
        """
    elif tclick == '3':
        goodslist = typelist.goodsinfo_set.order_by('-gclick')
        """
        实际运行代码应为
        goodslist = typelist.goodsinfo_set.order_by('gclick')
        """
    # 创建Paginator对象,每页显示15条数据，参数1为查找的对象集，参数2为每页显示多少条数据
    paginator = Paginator(goodslist,15)
    # 获取page对象,参数为页码
    pa = paginator.page(int(tindex))
    # 查询登录状态
    uname = request.session.get('username')

    # 推荐列表
    goodslist1 = typelist.goodsinfo_set.order_by('gclick')[0:2]
    """实际运行代码typelist.goodsinfo_set.order_by('gclick')[0:2]"""

    # 查找用户购买商品的数量
    uname = request.session.get('username')
    CartList = 0
    if uname != None:
        # print uname
        # 根据用户名称查找用户id
        User_id = UserInfo.objects.get(uname=uname).id
        # 查找购物车商品的数量
        CartList = len(CartInfo.objects.filter(user_id=User_id))
        # print CartList

    content = {
        # page对象
        'pa':pa,
        #排序规则
        'tclick':tclick,
        #id
        'id':tid,
        'uname':uname,
        'gl':goodslist1,
        'cartlen': CartList,
    }
    return render(request,'df_goods/list.html',content)

# 商品详情页面
def details(request,tid):
    # 查找对应id的商品
    goods = GoodsInfo.objects.filter(id = int(tid))[0]

    # 新品推荐的两个商品
    # 查询属于的typeinfo对象
    type = TypeInfo.objects.filter(id = goods.gtype_id)[0].goodsinfo_set.order_by('id')[0:2]

    """
    实际运行代码
    type = TypeInfo.objects.filter(id=goods.gtype_id)[0].goodsinfo_set.order_by('id')[0:2]
    """


    # 记录最近浏览的商品
    # 查询是否记录的浏览商品
    goods_id = request.COOKIES.get('goods_ids','')
    goods_id1 = str(goods_id)
    goods_id_str = ''
    # 如果未查询到记录
    if goods_id1 == '':
        #直接把商品的id加入到字符串
        goods_id_str = str(tid)
    else:#查询到了记录
        #分割字符串
        goods_str = goods_id1.split(',')
        # print goods_str
        #判断是否已经存在相同id的商品
        if str(tid) in goods_str:
            # print tid
            #如果经常存在，则删除
            goods_str.remove(str(tid))

        #拼接为字符串
        goods_str.insert(0,str(tid))
        if len(goods_str) >= 7:
            goods_str.remove(goods_str[5])
        goods_id_str = ','.join(goods_str)
    # print goods_str

    goods.gclick += 1
    goods.save()

    # 查找用户购买商品的数量
    uname = request.session.get('username')
    CartList = 0
    if uname != None:
        # 根据用户名称查找用户id
        User_id = UserInfo.objects.get(uname=uname).id
        # 查找购物车商品的数量
        CartList = len(CartInfo.objects.filter(user_id=User_id))

    uname = request.session.get('username')
    content = {
        'goods':goods,
        'type':type,
        'uname':uname,
        'cartlen': CartList,

    }
    respon = render(request,'df_goods/detail.html',content)
    # 最近浏览写入cookie
    respon.set_cookie('goods_ids',goods_id_str)

    return respon