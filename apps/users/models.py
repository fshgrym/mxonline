# -*- coding:utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser #我们想继承django系统默认的表
from django.utils.six import python_2_unicode_compatible


@python_2_unicode_compatible
class UserProfile(AbstractUser):#覆盖原有的user表
    nick_name=models.CharField(max_length=50,verbose_name=u'昵称',default='')
    birday=models.DateField(verbose_name=u'生日',null=True,blank=True)
    gender=models.CharField(max_length=6, choices=(('male',u'男'),('female',u'女')),default='female')
    address=models.CharField(max_length=100,default=u'')
    mobile=models.CharField(max_length=11,null=True,blank=True)
    image=models.ImageField(upload_to='image/%Y/%m',default=u'image/default.png',max_length=100)

    class Meta:
        verbose_name_plural=verbose_name='用户信息'

    def __str__(self):
        return self.username

    def get_unread_num(self):
        #获取用户未读信息
        from operations.models import UserMessage #放在这里的原因是避免循环引用，调用了才去导入
        return UserMessage.objects.filter(user=self.id,has_read=False).count()



@python_2_unicode_compatible
class EmailVerifyRecord(models.Model):#找回密码功能
    code=models.CharField(max_length=200,verbose_name=u'验证码')
    email=models.EmailField(max_length=50,verbose_name=u'邮箱')
    send_type=models.CharField(choices=(('register',u'注册'),('forget',u'找回密码'),('upemail',u'修改邮箱')),max_length=10,verbose_name=u'验证码类型')
    send_time=models.DateTimeField(default=datetime.now,verbose_name=u'发送时间')

    class Meta:
        verbose_name_plural=verbose_name=u'邮箱验证码'

    def __str__(self):
        return '{0}({1})'.format(self.code,self.email)

@python_2_unicode_compatible
class Banner(models.Model):
    title=models.CharField(max_length=100,verbose_name=u'标题')
    image=models.ImageField(upload_to='banner/%Y/%m',verbose_name=u'轮播图')
    url=models.URLField(max_length=200,verbose_name=u'访问链接')
    index=models.IntegerField(default=100,verbose_name=u'顺序')
    add_time=models.DateTimeField(default=datetime.now,verbose_name=u'添加时间')

    class Meta:
        verbose_name_plural=verbose_name=u'轮播图'

    def __str__(self):
        return self.title
