from django.shortcuts import render, redirect
import re
from user.models import *
from django.core.urlresolvers import reverse
from django.views.generic import View


class RegisterView(View):
    def get(self, request):
        # 注册页面
        return render(request, 'register.html')

    def post(self, request):
        # 注册处理

        # 接收数据
        username = request.POST.get('user_name')
        password = request.POST.get('pwd')
        cpwd = request.POST.get('cpwd')
        email = request.POST.get('email')
        allow = request.POST.get('allow')

        if not all([username, password, cpwd, email]):
            return render(request, 'register.html', {'errmsg': '数据不完整'})

        if password != cpwd:
            return render(request, 'register.html', {'errmsg': '两次密码不一致'})

        if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return render(request, 'register.html', {'errmsg': '邮箱格式不正确'})

        if allow != 'on':
            return render(request, 'register.html', {'errmsg': '请同意协议'})

        # 校验用户名是否重复
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = None

        if user:
            return render(request, 'register.html', {'errmsg': '用户名已存在'})

        # 业务处理，进行用户注册
        user = User.objects.create_user(username, email, password)
        user.is_active = 0
        user.save()

        # 返回应答，跳转到登录页面
        return redirect(reverse('user:login'))


def login(request):
    return render(request, 'login.html')


def login_handler(request):
    return render(request, 'login.html')
