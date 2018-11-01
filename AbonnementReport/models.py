# coding=utf-8

from django.db import models


class UserClass(models.Model):
    userName = models.CharField(max_length=30)
    passWord = models.CharField(max_length=30)
    emailAddr = models.CharField(max_length=30)
    productLine = models.CharField(max_length=30)
