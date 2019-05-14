# coding:utf8

from django.http import HttpResponseRedirect

def user_verification_login(func):
    def login(request,*args,**kwargs):
        # 判断是否有登录状态
        # print 1
        if request.session.get('username'):
            # 如果有登录状态，直接运行视图
            return func(request,*args,**kwargs)
        else:
            #如果没有登录，则重定向到登录页面
            # 创建重定向
            red = HttpResponseRedirect('/user/login/')
            '''
            向cookie中写入当前的地址

            '''
            red.set_cookie('url',request.get_full_path())
            # print request.get_full_path()
            return red
    return login