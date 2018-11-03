# coding=utf-8
"""AbonnementReport URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import url

from AbonnementReport import view

urlpatterns = [
    # 默认为登录界面
    url(r"^$", view.login),
    url(r"^login", view.login),

    # 注册界面
    url(r"^regist", view.regist),

    # 用户登录
    url(r"^userLogin", view.userLogin),

    # 用户注册
    url(r"^userRegist", view.userRegist),

    # 主页面
    url(r"^index", view.index),

    # 退出登录
    url(r"^logout", view.logout),

    # 添加版本
    url(r"^addVersion", view.addVersion),

    # 删除版本
    url(r"^delVersion", view.delVersion),

    # 均不匹配，清理所有session，进入登录界面
    url(r"^", view.logout),
]
