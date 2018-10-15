import re
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.views.generic import View
from user.models import *
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature
from MyItem import settings
from django.http import HttpResponse
from celery_tasks.tasks import task_send_mail
from django.contrib.auth import authenticate, login
from utils.user_util import *

from PIL import Image, ImageDraw, ImageFont
import random
from django.conf import settings
from io import BytesIO


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

        '''
        发送激活邮件，包含激活链接：http://ip:port//user/active/用户ID
        激活链接中需要包含用户的身份信息，并且要把身份信息进行加密
        '''

        # 加密用户的身份信息，生成激活token
        serializer = Serializer(settings.SECRET_KEY, 3600)
        info = {'confirm': user.id}
        token = serializer.dumps(info).decode()
        encryption_url = 'http://192.168.12.193:9520/user/active/%s' % token

        # 发邮件
        subject = '天天生鲜欢迎信息'  # 主题
        message = ''  # 文本内容
        sender = settings.EMAIL_FROM  # 发件人
        receiver = [email]  # 收件人
        html_message = '<h1>%s,欢迎您成为天天生鲜注册会员</h1>请点击下面的链接激活您的账户<br/><a = href="%s">%s</a>' % (
            username, encryption_url, encryption_url)

        task_send_mail.delay(subject, message, sender, receiver, html_message)  # 发送

        # 返回应答，跳转到登录页面
        return redirect(reverse('user:login'))


class ActiveView(View):
    '''用户激活'''

    def get(self, request, token):
        '''进行用户激活'''
        # 进行解密，获取要激活的用户信息
        serializer = Serializer(settings.SECRET_KEY, 3600)
        try:
            info = serializer.loads(token)
            # 获取待激活用户的id
            user_id = info['confirm']

            # 根据id获取用户信息
            user = User.objects.get(id=user_id)
            user.is_active = 1
            user.save()

            # 跳转到登录页面
            return redirect(reverse('user:login'))
        except SignatureExpired as e:
            return HttpResponse('激活链接已过期！')
        except BadSignature as e:
            return HttpResponse('激活链接非法！')


class LoginView(View):
    '''登录'''

    def get(self, request):
        '''显示登录页面'''
        # 判断是否记住了用户名
        if 'username' in request.COOKIES:
            username = request.COOKIES.get('username')
            checked = 'checked'
        else:
            username = ''
            checked = ''

        # 使用模板
        return render(request, 'login.html', {'username': username, 'checked': checked})

    def post(self, request):
        '''登录校验'''
        # 接收数据
        username = request.POST.get('username')
        password = request.POST.get('pwd')
        validate = request.POST.get('validate')

        print(validate)

        # 校验数据
        if not all([username, password, validate]):
            return render(request, 'login.html', {'errmsg': '数据不完整'})

        # 业务处理：用户登录
        user = authenticate(username=username, password=password)

        if user is not None:
            # 校验验证码
            ret = request.session.get('validate_code', '').lower()
            print(ret)
            if validate.lower() == ret:
                # 用户名密码正确
                if user.is_active:
                    # 用户已激活，记录用户的登录状态
                    login(request, user)

                    next_url = request.GET.get('next')
                    if next_url:
                        # 跳转到登录前的页面
                        response = redirect(next_url)
                    else:
                        # 跳转到首页
                        response = redirect(reverse('goods:index'))

                    # 判断是否需要记住用户名
                    remember = request.POST.get('remember')

                    if remember == 'on':
                        # 记住用户名
                        response.set_cookie('username', username, max_age=7 * 24 * 3600)
                    else:
                        response.delete_cookie('username')

                    # 返回response
                    return response
                else:
                    # 用户未激活
                    return render(request, 'login.html', {'errmsg': '账户未激活'})
            else:
                # 验证码错误
                return render(request, 'login.html', {'errmsg': '验证码错误'})
        else:
            # 用户名或密码错误
            return render(request, 'login.html', {'errmsg': '用户名或密码错误'})


def validate_code(request):
    # 定义变量，用于画面的背景色、宽、高
    bgcolor = (random.randrange(20, 100), random.randrange(20, 100), 255)
    width = 100
    height = 25
    # 创建画面对象
    im = Image.new('RGB', (width, height), bgcolor)
    # 创建画笔对象
    draw = ImageDraw.Draw(im)
    # 调用画笔的point()函数绘制噪点
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)
    # 定义验证码的备选值
    str1 = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0'
    # 随机选取4个值作为验证码
    rand_str = ''
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]

    # 构造字体对象
    font = ImageFont.truetype(settings.FONT_STYLE, 23)
    # 构造字体颜色
    fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
    # 绘制4个字
    for i in range(4):
        draw.text((5 + i * 25, 2), rand_str[i], font=font, fill=fontcolor)
    # 释放画笔
    del draw
    # 存入session，用于做进一步验证
    request.session['validate_code'] = rand_str
    # 内存文件操作
    buf = BytesIO()
    # 将图片保存在内存中，文件类型为png
    im.save(buf, 'png')
    # 将内存中的图片数据返回给客户端，MIME类型为图片png
    return HttpResponse(buf.getvalue(), 'images/png')


class UserInfoView(LoginRequiredMixin, View):
    '''用户中心-信息页'''

    def get(self, request):
        context = {'page': '1'}
        return render(request, 'user_center_info.html', context)


class UserOrderView(LoginRequiredMixin, View):
    '''用户中心-订单页'''

    def get(self, request):
        context = {'page': '2'}
        return render(request, 'user_center_order.html', context)


class UserAddressView(LoginRequiredMixin, View):
    '''用户中心-地址页'''

    def get(self, request):
        context = {'page': '3'}
        return render(request, 'user_center_site.html', context)
