# coding=utf-8

from django.db import models


class UserClass(models.Model):
    """
    用户数据表
    """
    userName = models.CharField(max_length=30)
    passWord = models.CharField(max_length=30)
    emailAddr = models.CharField(max_length=30)
    productLine = models.CharField(max_length=30)


class UserAuth(models.Model):
    """
    用户权限表
    """
    userName = models.CharField(max_length=30)
    userAuth = models.CharField(max_length=30)


class ProductVersion(models.Model):
    """
    版本数据表
    """
    versionName = models.CharField(max_length=30)


class AbonnementClass(models.Model):
    """
    订阅数据表
    """
    versionName = models.CharField(max_length=30)
    userName = models.CharField(max_length=30)
    emailAddr = models.CharField(max_length=30)
