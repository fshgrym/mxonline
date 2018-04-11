#!/usr/bin/env python
# -*- coding:utf-8 -*- 
# Author:fsh
#time:'2018/2/27 19:46:19下午'
from django.conf.urls import url
from .views import UserinfoView,UploadImageViwe,ModifyPwdView,SendEmailCodeView,UpdateEmailView,MyCourseView
from .views import MyFavCourseView,MyFavOrgView,MyFavTeacherView,MymessageView
urlpatterns = [
    url(r'^info/$',UserinfoView.as_view(),name='user_info'),#用户个人信息
    url(r'^image/upload/$',UploadImageViwe.as_view(),name='image'),#用户上传头像
    url(r'^update/pwd/$',ModifyPwdView.as_view(),name='update_pwd'),#用户修改密码
    url(r'^sendemail/code/$',SendEmailCodeView.as_view(),name='sendemail_code'),#发送邮件验证码
    url(r'^update/email/$',UpdateEmailView.as_view(),name='update_email'),#修改个人邮箱验证接口
    url(r'^mycourse/$',MyCourseView.as_view(),name='mycourse'),
    url(r'^fav/course/$',MyFavCourseView.as_view(),name='fav_course'),
    url(r'^fav/org/$',MyFavOrgView.as_view(),name='fav_org'),
    url(r'^fav/teacher/$',MyFavTeacherView.as_view(),name='fav_teacher'),
    url(r'^message/$',MymessageView.as_view(),name='message'),

]