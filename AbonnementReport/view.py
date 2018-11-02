# coding=utf-8

from django.shortcuts import render, redirect

from AbonnementReport.models import UserClass, UserAuth


# 登陆页
def login(request):
    # 若存在"loginErr"session，跳转登录页带err
    if "loginErr" in request.session:
        errMsg = request.session["loginErr"]
        del request.session["loginErr"]
        return render(request, 'login.html', {'err': errMsg})
    # 若存在"username"session，跳转首页；否则跳转登录页
    if "username" in request.session:
        return redirect('/index')
    return render(request, 'login.html')


# 注册页
def regist(request):
    # 若存在"registErr"session，跳转注册页带err
    if "registErr" in request.session:
        errMsg = request.session["registErr"]
        del request.session["registErr"]
        return render(request, 'regist.html', {'err': errMsg})
    # 若存在"username"session，跳转首页
    if "username" in request.session:
        return redirect('/index')
    return render(request, 'regist.html')


# 用户登录动作
def userLogin(request):
    # 若未传入用户名和密码，跳转登录页面
    if "username" not in request.POST and "password" not in request.POST:
        request.session["loginErr"] = '请输入用户名和密码'
        return redirect('/login')

    # 验证用户名、密码是否正确
    username = request.POST['username']

    # 查询结果为0，不存在此用户名的用户
    if len(UserClass.objects.filter(userName=username)) == 0:
        request.session["loginErr"] = '用户名或密码错误'
        return redirect('/login')

    # 用户名存在，匹配密码，不正确返回登录页面
    user = UserClass.objects.get(userName=username)
    if user.passWord != request.POST['password']:
        request.session["loginErr"] = '用户名或密码错误'
        return redirect('/login')

    # 获取用户权限，根据权限显示首页内容
    userAuth = UserAuth.objects.get(userName=username)

    # 设置session，并设定12小时session过期
    request.session["username"] = username
    request.session["productLine"] = user.productLine
    request.session["userAuth"] = userAuth.userAuth
    request.session.set_expiry(60 * 60 * 12)
    return redirect('/index')


# 用户注册动作
def userRegist(request):
    # 未传入用户名、密码、邮箱，跳转注册页面
    if "username" not in request.POST and "password" not in request.POST and "email" not in request.POST:
        request.session["registErr"] = '请输入用户名、密码、邮箱'
        return redirect('/regist')
    # 若用户存在直接，返回False
    if isExistUser(request) is False:
        # 设置session，使用重定向
        request.session["registErr"] = '用户名或邮箱已存在'
        return redirect('/regist')

    # 用户不存在，注册成功
    user = UserClass(userName=request.POST['username'],
                     passWord=request.POST['password'],
                     emailAddr=request.POST['email'],
                     productLine=request.POST['productline'])
    user.save()

    # 新注册用户，权限均为user
    admin = UserAuth(userName=request.POST['username'], userAuth="user")
    admin.save()

    # 设置session，并跳转到首页
    request.session["username"] = request.POST['username']
    request.session["productLine"] = request.POST['productline']
    request.session["userAuth"] = "user"
    request.session.set_expiry(60 * 30)
    return redirect('/index')


# 判断用户是否存在
def isExistUser(request):
    # 查询用户名和邮箱
    nameQureySet = UserClass.objects.filter(userName=request.POST['username'])
    mailQureySet = UserClass.objects.filter(emailAddr=request.POST['email'])
    # 邮箱地址和用户名同时没有注册过，返回True，表示可以注册；否则返回False，表示不能注册
    if len(nameQureySet) == 0 and len(mailQureySet) == 0:
        return True
    return False


# 首页
def index(request):
    if "username" in request.session:
        return render(request, 'index.html',
                      {'username': request.session["username"],
                       'productLine': request.session["productLine"],
                       'userAuth': request.session["userAuth"]})
    else:
        return redirect('/login')


# 退出登录
def logout(request):
    request.session.clear()
    return redirect('/login')
