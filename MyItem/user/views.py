import re
from django.shortcuts import *
from django.core.urlresolvers import reverse
from django.views.generic import View
from user.models import *
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature
from MyItem import settings
from django.http import *
from celery_tasks.tasks import task_send_mail
from django.contrib.auth import authenticate, login, logout
from utils.user_util import *
from redis import StrictRedis
from goods.models import *

from PIL import Image, ImageDraw, ImageFont
import random
from django.conf import settings
from io import BytesIO
from django.core import serializers


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

        # 校验数据
        if not all([username, password, validate]):
            return render(request, 'login.html', {'errmsg': '数据不完整'})

        # 业务处理：用户登录
        user = authenticate(username=username, password=password)

        if user is not None:
            # 校验验证码
            ret = request.session.get('validate_code', '').lower()
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


class LogoutView(View):
    '''退出登录'''

    def get(self, request):
        '''退出登录'''
        # 清除用户的session信息
        logout(request)
        # 跳转到首页
        return redirect(reverse('user:login'))


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


def checkusername(request):
    user_name = request.GET.get('user_name')
    if user_name == '':
        return HttpResponse(-1)
    elif User.objects.filter(username=user_name).exists():
        return HttpResponse(1)
    else:
        return HttpResponse(0)


class UserInfoView(LoginRequiredMixin, View):
    '''用户中心-信息页'''

    def get(self, request):
        # 获取登录用户对应User对象
        user = request.user
        # 获取用户的默认收货地址
        try:
            address = Address.objects.get(user=user, is_default=True)
        except Address.DoesNotExist:
            # 不存在默认收货地址
            address = None

        # 读取历史记录
        # 连接redis
        conn = StrictRedis('192.168.12.193')
        history = conn.lrange('history_%d' % user.id, 0, -1)
        print(history)

        goodskus = GoodsSKU.objects.filter(id__in=history)
        print(goodskus)

        context = {'page': '1', 'address': address, 'goodskus': goodskus}
        return render(request, 'user_center_info.html', context)


class UserOrderView(LoginRequiredMixin, View):
    '''用户中心-订单页'''

    def get(self, request):
        context = {'page': '2'}
        return render(request, 'user_center_order.html', context)


class UserAddressView(LoginRequiredMixin, View):
    '''用户中心-地址页'''

    def get(self, request):
        '''显示'''
        # 获取登录用户对应User对象
        user = request.user
        # 获取用户的默认地址
        try:
            address = Address.objects.get(user=user, is_default=True)
        except Address.DoesNotExist:
            # 不存在默认收获地址
            address = None

        # 数据字典
        context = {'page': '3', 'address': address}
        return render(request, 'user_center_site.html', context)

    def post(self, request):
        '''地址的添加'''

        # 获取登录用户对应User对象
        user = request.user
        try:
            address = Address.objects.get(user=user, is_default=True)
        except Address.DoesNotExist:
            # 不存在默认收货地址
            address = None

        # 数据字典
        context = {'page': '3', 'address': address, 'errmsg': ''}

        # 接收数据
        receiver = request.POST.get('receiver')
        province_id = request.POST.get('province_id')
        city_id = request.POST.get('city_id')
        town_id = request.POST.get('town_id')
        addr = request.POST.get('addr')
        zip_code = request.POST.get('zip_code')
        phone = request.POST.get('phone')

        # 查找地址信息
        if province_id == '0':
            province = ''
        else:
            province = Province.objects.filter(pk=province_id)[0].name

        if city_id == '0':
            city = ''
        else:
            city = City.objects.filter(pk=city_id)[0].name

        if town_id == '0':
            town = ''
        else:
            town = Town.objects.filter(pk=town_id)[0].name

        # 拼接地址
        addr_all = province + city + town + addr

        # 校验数据
        if not all([receiver, addr_all, phone, ]):
            context['errmsg'] = '数据不完整'
            return render(request, 'user_center_site.html', context)

        # 校验手机号
        if not re.match(r'^(13[0-9]|14[579]|15[0-3,5-9]|16[6]|17[0135678]|18[0-9]|19[89])\d{8}$', phone):
            context['errmsg'] = '手机格式不正确'
            return render(request, 'user_center_site.html', context)

        '''
        业务处理：地址添加
        用户新添加的地址作为默认收货地址，如果原来有默认地址，要取消
        获取用户的默认收货地址
        '''

        address.is_default = False

        # 添加地址
        Address.objects.create(
            user=user,
            receiver=receiver,
            addr=addr_all,
            zip_code=zip_code,
            phone=phone,
            is_default=True
        )

        address.save()

        # 返回应答，刷新地址页面
        return redirect(reverse('user:address'))


# 获取所有的省份，转成json格式
def get_all_province(request):
    province_list = Province.objects.all()
    content = {
        'province_list': serializers.serialize('json', province_list)
    }
    return JsonResponse(content)


# 根据省份的code获取城市
def get_city_by_province_code(request):
    province_id = request.GET.get('province_id')
    province_code = Province.objects.filter(pk=province_id)[0].code
    city_list = City.objects.filter(province_code=province_code)
    content = {
        'city_list': serializers.serialize('json', city_list)
    }
    return JsonResponse(content)


# 根据城市的code获取区县
def get_town_by_city_code(request):
    city_id = request.GET.get('city_id')
    city_code = City.objects.filter(pk=city_id)[0].code
    town_list = Town.objects.filter(city_code=city_code)
    content = {
        'town_list': serializers.serialize('json', town_list)
    }
    return JsonResponse(content)
