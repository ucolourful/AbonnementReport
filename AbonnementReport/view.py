# coding=utf-8


from __future__ import print_function
from django.shortcuts import render, redirect
from django.http import HttpResponse
import json

from AbonnementReport.models import UserClass, UserAuth, ProductVersion, AbonnementClass


# 登陆页
def login(request):
    # 若存在"loginErr"session，跳转登录页带err并删除"loginErr"session
    if "loginErr" in request.session:
        errMsg = request.session["loginErr"]
        del request.session["loginErr"]
        return render(request, 'login.html', {'err': errMsg})

    # 若存在"username"session，跳转首页；否则跳转登录页
    if "username" in request.session:
        return redirect('/index')

    return render(request, 'login.html')


# 用户登录动作
def userLogin(request):
    # 非正常请求，跳转到登录页
    if "username" not in request.POST and "password" not in request.POST:
        return redirect('/login')

    # 不存在此用户
    if len(UserClass.objects.filter(userName=request.POST['username'])) == 0:
        return HttpResponse(json.dumps({"status": 1, "msg": "用户名或密码错误"}), content_type="application/json")

    # 用户名存在，匹配密码，不正确返回登录页面
    user = UserClass.objects.get(userName=request.POST['username'])
    if user.passWord != request.POST['password']:
        return HttpResponse(json.dumps({"status": 1, "msg": "用户名或密码错误"}), content_type="application/json")

    # 获取用户权限，根据权限显示首页内容
    userAuth = UserAuth.objects.get(userName=request.POST['username'])

    # 设置session，并设定12小时session过期
    request.session["username"] = user.userName
    request.session["productLine"] = user.productLine
    request.session["userAuth"] = userAuth.userAuth
    request.session.set_expiry(60 * 60 * 12)
    return HttpResponse(json.dumps({"status": 0, "msg": "登录成功！即将跳转到首页！"}), content_type="application/json")


# 注册页
def regist(request):
    # 若存在"registErr"session，跳转注册页带err并删除"registErr"session
    if "registErr" in request.session:
        errMsg = request.session["registErr"]
        del request.session["registErr"]
        return render(request, 'regist.html', {'err': errMsg})

    # 若存在"username"session，跳转首页
    if "username" in request.session:
        return redirect('/index')

    return render(request, 'regist.html')


# 用户注册动作
def userRegist(request):
    # 非正常请求，跳转到注册页
    if "username" not in request.POST and "password" not in request.POST and "password2" not in request.POST and "email" not in request.POST and "productline" not in request.POST:
        return redirect('/regist')

    # 若用户名存在，返回"用户名或邮箱已存在"
    if len(UserClass.objects.filter(userName=request.POST["username"])) != 0 \
            or len(UserClass.objects.filter(emailAddr=request.POST["email"])) != 0:
        return HttpResponse(json.dumps({"status": 1, "msg": "用户名或邮箱已存在"}), content_type="application/json")

    # 用户不存在，注册成功
    user = UserClass(userName=request.POST['username'],
                     passWord=request.POST['password'],
                     emailAddr=request.POST['email'],
                     productLine=request.POST['productline'])
    user.save()

    # 新注册用户，权限均为user；简单处理
    # 为开发便利，若admin为注册用户，设为admin权限
    if "admin" in request.POST['username']:
        ua = UserAuth(userName=request.POST['username'], userAuth="admin")
    else:
        ua = UserAuth(userName=request.POST['username'], userAuth="user")
    ua.save()

    # 设置session，并跳转到首页
    request.session["username"] = request.POST['username']
    request.session["productLine"] = request.POST['productline']
    request.session["userAuth"] = ua.userAuth
    request.session.set_expiry(60 * 60 * 12)
    return HttpResponse(json.dumps({"status": 0, "msg": "注册成功！即将跳转到首页！"}), content_type="application/json")


# 首页
def index(request):
    # 非登录用户，返回登录页面
    if "username" not in request.session or "userAuth" not in request.session or "productLine" not in request.session:
        return redirect('/login')

    # 登录用户，获取订阅信息
    acList = []
    listData = AbonnementClass.objects.filter(userName=request.session["username"])
    for l in listData:
        acList.append(l.versionName)
    return render(request, 'index.html',
                  {'username': request.session["username"],
                   'productLine': request.session["productLine"],
                   'userAuth': request.session["userAuth"],
                   'versionList': ProductVersion.objects.all(),
                   'acList': acList})


# 添加版本
def addVersion(request):
    # 非登录用户，返回登录页面
    if "username" not in request.session or "userAuth" not in request.session or "productLine" not in request.session:
        return redirect('/login')

    # admin具有添加权限，versionName为必需参数；判断是否存在versionName版本
    if request.session["userAuth"] == "admin" and "versionName" in request.POST:
        if request.POST["versionName"] != "":
            versionNameList = ProductVersion.objects.filter(versionName=request.POST["versionName"])
            if len(versionNameList) == 0:
                proVersion = ProductVersion(versionName=request.POST["versionName"])
                proVersion.save()
                return HttpResponse(json.dumps({"status": 0, "msg": "添加版本成功！"}), content_type="application/json")
    return HttpResponse(json.dumps({"status": 1, "msg": "添加版本失败！请确认权限或版本是否已经存在！"}), content_type="application/json")


# 删除版本
def delVersion(request):
    # 非登录用户，返回登录页面
    if "username" not in request.session or "userAuth" not in request.session or "productLine" not in request.session:
        return redirect('/login')

    # admin具有删除权限，versionID为必需参数；判断是否存在versionID版本
    if request.session["userAuth"] == "admin" and "versionID" in request.POST:
        if request.POST["versionID"] != "":
            versionIDList = ProductVersion.objects.filter(id=int(request.POST["versionID"]))
            if len(versionIDList) != 0:
                # 删除订阅人信息
                proVersion = ProductVersion.objects.get(id=int(request.POST["versionID"]))
                abList = AbonnementClass.objects.filter(versionName=proVersion.versionName)
                for ab in abList:
                    ab.delete()
                proVersion.delete()
                return HttpResponse(json.dumps({"status": 0, "msg": "删除版本成功！"}), content_type="application/json")
    return HttpResponse(json.dumps({"status": 1, "msg": "删除版本失败！请确认权限或版本是否已删除！"}), content_type="application/json")


# 订阅/取消订阅
def abonnementReport(request):
    # 非登录用户，返回登录页面
    if "username" not in request.session or "userAuth" not in request.session or "productLine" not in request.session:
        return redirect('/login')

    # 未传入versionID
    if "versionID" not in request.POST or "doAction" not in request.POST:
        return HttpResponse(json.dumps({"status": 1, "msg": "操作失败！请重新登录进行尝试！"}), content_type="application/json")

    # 判断，是否存在versionID的版本、用户是否存在，任意不存在返回首页
    versionIDList = ProductVersion.objects.filter(id=int(request.POST["versionID"]))
    userList = UserClass.objects.filter(userName=request.session["username"])
    if len(versionIDList) == 0 or len(userList) == 0:
        return HttpResponse(json.dumps({"status": 1, "msg": "操作失败！请重新登录进行尝试！"}), content_type="application/json")

    # 获取用户、版本和订阅表信息
    proVersion = ProductVersion.objects.get(id=int(request.POST["versionID"]))
    user = UserClass.objects.get(userName=request.session["username"])
    acList = AbonnementClass.objects.filter(versionName=proVersion.versionName, userName=user.userName,
                                            emailAddr=user.emailAddr)

    # "doAction==1"用户进行订阅操作；并判断该用户是否订阅过此版本，订阅过则返回到首页
    if "1" == request.POST["doAction"] and len(acList) == 0:
        # 保存订阅信息到订阅数据表
        ac = AbonnementClass(versionName=proVersion.versionName, userName=user.userName, emailAddr=user.emailAddr)
        ac.save()
        return HttpResponse(json.dumps({"status": 0, "msg": "订阅成功！"}), content_type="application/json")

    # "doAction==0"用户进行取消订阅操作；并判断用户是否订阅过此版本，未订阅则返回到首页
    elif "0" == request.POST["doAction"] and len(acList) == 1:
        ac = AbonnementClass.objects.get(versionName=proVersion.versionName, userName=user.userName,
                                         emailAddr=user.emailAddr)
        ac.delete()
        return HttpResponse(json.dumps({"status": 0, "msg": "取消订阅成功！"}), content_type="application/json")
    return HttpResponse(json.dumps({"status": 1, "msg": "操作失败！请重新登录进行尝试！"}), content_type="application/json")


# 更新用户信息页
def userSetting(request):
    # 非登录用户，返回登录页面
    if "username" not in request.session or "userAuth" not in request.session or "productLine" not in request.session:
        return redirect('/login')

    # 判断用户是否存在，不存在返回登录页
    userList = UserClass.objects.filter(userName=request.session["username"])
    if len(userList) != 1:
        return redirect('/logout')

    # 获取用户
    user = UserClass.objects.get(userName=request.session["username"])

    # 到更新页
    return render(request, 'setting.html',
                  {'user': user})


# 更新用户信息操作
def userUpdate(request):
    # 非登录用户，返回登录页面
    if "username" not in request.session or "userAuth" not in request.session or "productLine" not in request.session:
        return redirect('/login')

    # 非正常请求，跳转到登录页面
    if "username" not in request.POST and "password" not in request.POST and "password2" not in request.POST and "email" not in request.POST and "productline" not in request.POST:
        return redirect('/login')

    # 首先获取到用户原信息
    user = UserClass.objects.get(id=int(request.POST["userID"]))

    # 对比原用户名和新用户名
    if user.userName != request.POST["username"]:
        if len(UserClass.objects.filter(userName=request.POST["username"])) > 0:
            return HttpResponse(json.dumps({"status": 1, "msg": "用户名已存在！"}), content_type="application/json")

    if user.emailAddr != request.POST["email"]:
        if len(UserClass.objects.filter(emailAddr=request.POST["email"])) > 0:
            return HttpResponse(json.dumps({"status": 1, "msg": "邮箱已存在！"}), content_type="application/json")

    # 更新订阅表
    acList = AbonnementClass.objects.filter(userName=user.userName, emailAddr=user.emailAddr)
    if len(acList) > 0:
        for ac in acList:
            ac.userName = request.POST["username"]
            ac.emailAddr = request.POST["email"]
            ac.save()

    # 更新权限表
    uaList = UserAuth.objects.filter(userName=user.userName)
    if len(uaList) > 0:
        for ua in uaList:
            ua.userName = request.POST["username"]
            ua.save()

    # 更新用户表
    user.userName = request.POST["username"]
    user.passWord = request.POST["password"]
    user.emailAddr = request.POST["email"]
    user.productLine = request.POST["productline"]
    user.save()

    # 更新session
    request.session["username"] = request.POST["username"]
    request.session["productLine"] = request.POST["productline"]
    return HttpResponse(json.dumps({"status": 0, "msg": "修改信息成功！即将跳转到首页~"}), content_type="application/json")


# 退出登录
def logout(request):
    # 清空所有session
    request.session.clear()
    return redirect('/login')


# 查看订阅人(api接口，不判断是否登录)
def viewVersionUsers(request):
    resp = {"status": 1, "msg": {}}

    # 单个版本
    if "versionName" in request.GET:
        versionName = request.GET["versionName"]
        if versionName != "":
            resp["msg"] = {versionName: []}
            acList = AbonnementClass.objects.filter(versionName=versionName)
            for ac in acList:
                resp["status"] = 0
                resp["msg"][versionName].append(ac.emailAddr)

    # 所有版本
    else:
        acList = AbonnementClass.objects.all()
        if len(acList) > 0:
            for ac in acList:
                if resp["msg"].has_key(ac.versionName) is False:
                    resp["msg"][ac.versionName] = [ac.emailAddr]
                else:
                    resp["msg"][ac.versionName].append(ac.emailAddr)
        else:
            versionList = ProductVersion.objects.all()
            for vl in versionList:
                if resp["msg"].has_key(vl.versionName) is False:
                    resp["msg"][vl.versionName] = []

    return HttpResponse(json.dumps(resp), content_type="application/json")
